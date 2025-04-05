"""
Main FastAPI application module.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.databases import dict_db, main_db
from app.routes import analysis, auth, user
from app.schemas import MobileInfoSchema

# Create FastAPI app
app = FastAPI(tittle=settings.APP_NAME)

# Authorized origins for CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(user.router, tags=["User"])


# Mobile info route
@app.get("/mobile", response_model=MobileInfoSchema)
def get_mobile_info() -> MobileInfoSchema:
    """
    Retrieves mobile application version information.

    Returns:
        MobileInfoSchema: Minimum version requirements for iOS and Android.
    """
    return MobileInfoSchema(
        min_version_ios=settings.MIN_VERSION_IOS,
        min_version_android=settings.MIN_VERSION_ANDROID,
    )


# Init databases on startup
@app.on_event("startup")
async def startup() -> None:
    """
    Startup event handler, initialize the databases.
    """
    await dict_db.init_db()
    await main_db.init_db()
