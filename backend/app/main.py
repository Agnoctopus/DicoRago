"""
Main FastAPI application module.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import router

# Create FastAPI app
app = FastAPI()

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
app.include_router(router)


@app.on_event("startup")
async def startup() -> None:
    """
    Startup event handler, initialize the database.
    """
    await init_db()
