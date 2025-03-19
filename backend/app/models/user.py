"""
Module defining ORM models for user-related database entities.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.main_db import Base


class User(Base):
    """
    Represents a user of the application.

    Attributes:
        id (int): Unique identifier.
        created_at (datetime): Creation timestamp.
        google_id (Optional[str]): Google account identifier.
        apple_id (Optional[str]): Apple account identifier.
        email (str): Email address.
        name (str): Unique username.
        learned_words (List[LearnedWord]): Words learned by the user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    google_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    apple_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    learned_words: Mapped[List["LearnedWord"]] = relationship(
        "LearnedWord", back_populates="user"
    )


class LearnedWord(Base):
    """
    Represents a word learned by a user.

    Attributes:
        id (int): Unique identifier.
        written (str): Written form.
        learned (bool): Whether the word is learned.
        updated_at (datetime): Timestamp of the last update.
        user_id (int): Foreign key to the user.
        user (User): Associated user.
    """

    __tablename__ = "learned_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    written: Mapped[str] = mapped_column(String, nullable=False, index=True)
    learned: Mapped[bool] = mapped_column(Boolean, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # User relation
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped["User"] = relationship("User", back_populates="learned_words")

    # Index
    __table_args__ = (
        # To get last update
        Index("idx_user_updated", "user_id", "updated_at"),
        # To get learned count
        Index("idx_user_learned", "user_id", "learned"),
    )
