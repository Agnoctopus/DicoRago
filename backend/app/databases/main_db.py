"""
Main database configuration module.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Get database URL from app settings
DATABASE_URL = settings.DATABASE_MAIN_URL

# Create SQL engine and session maker
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(
    autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an async SQLAlchemy session.

    Yields:
        AsyncSession: An async SQLAlchemy session.
    """
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
