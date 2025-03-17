"""
Module defining ORM models for database backed user related objects.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.main_db import Base


class User(Base):
    """
    Represents a user of the application.

    Attributes:
        id (int): Unique identifier.
        google_id (Optional[str]): Google account identifier.
        apple_id (Optional[str]): Apple account identifier.
        email (str): User email address.
        name (str): Unique username.
        learned_words (List[LearnedWord]): Words learned by the user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    google_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    apple_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    learned_words: Mapped[List["LearnedWord"]] = relationship(
        "LearnedWord", back_populates="user"
    )


class LearnedWord(Base):
    """
    Represents a word learned by a user.

    Attributes:
        id (int): Unique identifier.
        written (str): The written word.
        created_at (datetime): Timestamp when the word was learned.
        user_id (int): Foreign key to the user.
        user (User): Associated user.
    """

    __tablename__ = "learned_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    written: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="learned_words")
