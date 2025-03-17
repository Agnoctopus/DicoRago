"""
Module defining ORM models for database backed dictionary related objects.
"""

from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databases.dict_db import Base


class Word(Base):
    """
    Represents a word.

    Attributes:
        id (int): Unique identifier.
        written (str): Written form.
        category (str): Word category.
        senses (List[Sense]): Associated senses.
    """

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    written: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    senses: Mapped[List["Sense"]] = relationship("Sense", back_populates="word")


class Sense(Base):
    """
    Represents a sense of a word.

    Attributes:
        id (int): Unique identifier.
        word_id (int): Foreign key to the related word.
        word (Word): Associated word.
        english_word (str): English form.
        english_definition (str): English definition.
        examples (List[Example]): Associated examples.
    """

    __tablename__ = "senses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id"))
    word: Mapped["Word"] = relationship("Word", back_populates="senses")
    english_word: Mapped[str] = mapped_column(String, nullable=False)
    english_definition: Mapped[str] = mapped_column(String, nullable=False)
    examples: Mapped[List["Example"]] = relationship("Example", back_populates="sense")


class Example(Base):
    """
    Represents an example usage of a sense.

    Attributes:
        id (int): Unique identifier.
        sense_id (int): Foreign key to the related sense.
        sense (Sense): Associated sense.
        category (str): Example category.
        example (str): Example text.
    """

    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sense_id: Mapped[int] = mapped_column(Integer, ForeignKey("senses.id"))
    sense: Mapped["Sense"] = relationship("Sense", back_populates="examples")
    category: Mapped[str] = mapped_column(String(16), nullable=False)
    example: Mapped[str] = mapped_column(String, nullable=False)
