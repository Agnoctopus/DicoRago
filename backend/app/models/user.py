"""
Module defining ORM models for user-related database entities.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
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
        picture (Optional[str]): Link to avatar picture.
        vocab_words (List[VocabWord]): Vocabulary words.
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
    picture: Mapped[str] = mapped_column(String, nullable=True)
    vocab_words: Mapped[List["VocabWord"]] = relationship(
        "VocabWord", back_populates="user"
    )


class VocabWord(Base):
    """
    Represents a word vocabulary word from a user.

    Attributes:
        id (int): Unique identifier.
        written (str): Written form.
        status (str): Satus of the words.
        updated_at (datetime): Timestamp of the last update.
        user_id (int): Foreign key to the user.
        user (User): Associated user.
    """

    __tablename__ = "vocab_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    written: Mapped[str] = mapped_column(String, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # User relation
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    user: Mapped["User"] = relationship("User", back_populates="vocab_words")

    # Index
    __table_args__ = (
        # To get last update
        Index("idx_user_updated", "user_id", "updated_at"),
        # To get status count
        Index("idx_user_status", "user_id", "status"),
    )
