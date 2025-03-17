"""
Module providing async repositories for database models.

Each repository provides methods to perform operations on specific records.
"""

from random import randint
from typing import List, Optional, Sequence

from sqlalchemy import case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Example, Sense, User, Word


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
        Retrieve a Word by id.

        Args:
            id (int): Word identifier.
            senses (bool): If True, eagerly load associated senses.

        Returns:
            Optional[Word]: Matching Word object.
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


class UserRepository:
    """
    Repository for User model.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the UserRepository.

        Args:
            session (AsyncSession): Async session used for operations.
        """
        self.session = session

    async def get_by_google_id(self, google_id: int) -> Optional[User]:
        """
        Retrieve an Example by a Google id.

        Args:
            google_id (int): Google identifier of the User.

        Returns:
            Optional[User]: Matching User object.
        """
        stmt = select(User).where(User.google_id == google_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        return user

    async def get_by_apple_id(self, apple_id: int) -> Optional[User]:
        """
        Retrieve an Example by a Google id.

        Args:
            apple_id (int): Apple identifier of the User.

        Returns:
            Optional[User]: Matching User object.
        """
        stmt = select(User).where(User.apple_id == apple_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        return user

    async def get_by_name(self, name: str) -> Optional[User]:
        """
        Retrieve an Example by a Google id.

        Args:
            name (int): Name the User.

        Returns:
            Optional[User]: Matching User object.
        """
        stmt = select(User).where(User.name == name)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        return user

    async def create_with_google(self, google_id: int, email: str, name: str) -> User:
        """
        Create a user with Google credentials.

        Args:
            google_id (int): Google account identifier.
            email (str): User email address.
            name (str): Desired user name.

        Returns:
            User: Newly created user object.
        """
        # Handle duplicate username
        duplicate_user = await self.get_by_name(name)
        if duplicate_user is not None:
            name += f"#{randint(1000,9999)}"

        # Create user object with Google credentials
        user = User(google_id=google_id, email=email, name=name)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_with_apple(self, apple_id: int, email: str, name: str) -> User:
        """
        Create a user with Apple credentials.

        Args:
            apple_id (int): Apple account identifier.
            email (str): User email address.
            name (str): Desired user name.

        Returns:
            User: Newly created user object.
        """
        # Handle duplicate username
        duplicate_user = await self.get_by_name(name)
        if duplicate_user is not None:
            name += f"#{randint(1000,9999)}"

        # Create user object with Apple credentials
        user = User(apple_id=apple_id, email=email, name=name)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
