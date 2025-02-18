"""
Module providing async repositories for database models.

Each repository provides methods to perform operations on specific records.
"""

from typing import List, Optional, Sequence

from sqlalchemy import case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Example, Sense, Word


class WordRepository:
    """
    Repository for Word model.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the WordRepository.

        Args:
            session (AsyncSession): Async session used for operations.
        """
        self.session = session

    async def get_by_id(self, word_id: int, senses: bool = False) -> Optional[Word]:
        """
        Retrieve Word(s) by id.

        Args:
            id (int): Word identifier.
            senses (bool): If True, eagerly load associated senses.

        Returns:
            Sequence[Word]: Matching Word objects.
        """
        stmt = select(Word).where(Word.id == word_id)
        if senses:
            stmt = stmt.options(selectinload(Word.senses))
        result = await self.session.execute(stmt)
        word = result.scalars().first()

        return word

    async def get_by_written(
        self, written: str, senses: bool = False
    ) -> Sequence[Word]:
        """
        Retrieve Word(s) by the 'written' value.

        Args:
            written (str): The written field value.
            senses (bool): If True, eagerly load associated senses.

        Returns:
            Sequence[Word]: Matching Word objects.
        """
        stmt = select(Word).where(Word.written == written)
        if senses:
            stmt = stmt.options(selectinload(Word.senses))
        result = await self.session.execute(stmt)
        words = result.scalars().all()

        return words

    async def get_by_writtens(
        self,
        writtens: List[str],
        senses: bool = False,
        order: bool = True,
    ) -> Sequence[Word]:
        """
        Retrieve Words whose 'written' field is in the provided list.

        Args:
            writtens (List[str]): All written values.
            senses (bool): If True, eagerly load associated senses.
            order (bool): If True, order results to match the writtens list.

        Returns:
            Sequence[Word]: Matching Word objects.
        """
        if len(writtens) == 0:
            return []

        stmt = select(Word).where(Word.written.in_(writtens))
        if order:
            order_expr = case(
                *[(Word.written == w, i) for i, w in enumerate(writtens)],
                else_=len(writtens),
            )
            stmt = stmt.order_by(order_expr)
        if senses:
            stmt = stmt.options(selectinload(Word.senses))
        result = await self.session.execute(stmt)
        words = result.scalars().all()

        return words


class SenseRepository:
    """
    Repository for Sense model.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the SenseRepository.

        Args:
            session (AsyncSession): Async session used for operations.
        """
        self.session = session

    async def get_by_word_id(self, word_id: int) -> Sequence[Sense]:
        """
        Retrieve Sense(s) by a Word id.

        Args:
            word_id (int): Identifier of the Word.

        Returns:
            Sequence[Sense]: Associated Sense objects.
        """
        stmt = select(Sense).where(Sense.word_id == word_id)
        result = await self.session.execute(stmt)
        senses = result.scalars().all()

        return senses


class ExampleRepository:
    """
    Repository for Example model.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the ExampleRepository.

        Args:
            session (AsyncSession): Async session used for operations.
        """
        self.session = session

    async def get_by_sense_id(self, sense_id: int) -> Sequence[Example]:
        """
        Retrieve Example(s) by a Sense id.

        Args:
            sense_id (int): Identifier of the Sense.

        Returns:
            Sequence[Example]: Associated Example objects.
        """
        stmt = select(Example).where(Example.sense_id == sense_id)
        result = await self.session.execute(stmt)
        examples = result.scalars().all()

        return examples
