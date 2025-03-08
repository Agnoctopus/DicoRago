"""
Module defining ORM models for database backed user related objects.
"""

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.main_db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    google_id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    learned_words: Mapped[List["LearnedWord"]] = relationship(
        "LearnedWord", back_populates="user"
    )


class LearnedWord(Base):
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
