"""
Module providing async repositories for database models.

Each repository provides methods to perform operations on specific records.
"""

from datetime import datetime
from random import randint
from typing import List, Optional, Sequence

from sqlalchemy import case, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, with_loader_criteria
from sqlalchemy.sql import functions

from app.models import Example, LearnedWord, Sense, SenseTranslation, User, Word
from app.schemas import LearnedWordSchema, VocStatusSchema


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

    async def get_by_id(
        self, word_id: int, senses: bool = False, language: str = "en_US"
    ) -> Optional[Word]:
        """
        Retrieve a Word by id.

        Args:
            id (int): Word identifier.
            senses (bool): If True, eagerly load associated senses.
            language (str): Language code to for translation.

        Returns:
            Optional[Word]: Matching Word object.
        """
        stmt = select(Word).where(Word.id == word_id)
        if senses:
            stmt = stmt.options(
                selectinload(Word.senses).selectinload(Sense.translations),
                with_loader_criteria(
                    SenseTranslation,
                    lambda translation: translation.language == language,
                    include_aliases=True,
                ),
            )

        result = await self.session.execute(stmt)
        word = result.scalars().first()

        return word

    async def get_by_written(
        self, written: str, senses: bool = False, language: str = "en_US"
    ) -> Sequence[Word]:
        """
        Retrieve Word(s) by its written form. Optionally loading associated its senses.

        Args:
            written (str): Written form.
            senses (bool): If True, eagerly load associated senses.
            language (str): Language code to for translation.

        Returns:
            Sequence[Word]: Matching Word objects.
        """
        stmt = select(Word).where(Word.written == written)

        if senses:
            stmt = stmt.options(
                selectinload(Word.senses).selectinload(Sense.translations),
                with_loader_criteria(
                    SenseTranslation,
                    lambda translation: translation.language == language,
                    include_aliases=True,
                ),
            )

        result = await self.session.execute(stmt)
        words = result.scalars().all()
        return words

    async def get_by_writtens(
        self,
        writtens: List[str],
        senses: bool = False,
        language: str = "en_US",
        order: bool = True,
    ) -> Sequence[Word]:
        """
        Retrieve Words whose 'written' field is in the provided list.

        Args:
            writtens (List[str]): All written values.
            senses (bool): If True, eagerly load associated senses.
            order (bool): If True, order results to match the writtens list.
            language (str): Language code to for translation.

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
            stmt = stmt.options(
                selectinload(Word.senses).selectinload(Sense.translations),
                with_loader_criteria(
                    SenseTranslation,
                    lambda translation: translation.language == language,
                    include_aliases=True,
                ),
            )
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

    async def get_by_word_id(
        self, word_id: int, language: Optional[str] = "en_US"
    ) -> Sequence[Sense]:
        """
        Retrieve Sense(s) by a Word id.

        Args:
            word_id (int): Identifier of the Word.
            language (Optional[str]): Language code to for translation.

        Returns:
            Sequence[Sense]: Associated Sense objects.
        """
        stmt = select(Sense).where(Sense.word_id == word_id)
        if language is None:
            stmt = stmt.options(selectinload(Sense.translations))
        else:
            stmt = stmt.options(
                selectinload(Sense.translations),
                with_loader_criteria(
                    SenseTranslation,
                    lambda translation: translation.language == language,
                    include_aliases=True,
                ),
            )
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

    async def get_by_google_id(self, google_id: str) -> Optional[User]:
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

    async def get_by_apple_id(self, apple_id: str) -> Optional[User]:
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

    async def create_with_google(
        self, google_id: str, email: str, name: str, picture: Optional[str] = None
    ) -> User:
        """
        Create a user with Google credentials.

        Args:
            google_id (int): Google account identifier.
            email (str): User email address.
            name (str): Desired user name.
            picture (Optional[str]): Link to avatar picture.

        Returns:
            User: Newly created user object.
        """
        # Handle duplicate username
        duplicate_user = await self.get_by_name(name)
        if duplicate_user is not None:
            name += f"#{randint(1000,9999)}"

        # Create user object with Google credentials
        user = User(google_id=google_id, email=email, name=name, picture=picture)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_with_apple(self, apple_id: str, email: str, name: str) -> User:
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


class VocRepository:
    """
    Repository for LearnedWord model.
    """

    def __init__(self, session: AsyncSession, user_id: int):
        """
        Initialize the vocabulary repository.

        Args:
            session (AsyncSession): Async session used for operations.
            user_id (int): User identifier for operation.
        """
        self.session = session
        self.user_id = user_id

    async def get_by_written(self, written: str) -> Optional[LearnedWord]:
        """
        Retrieve a LearnedWord record by its written form.

        Args:
            written (str): Written form of the word.

        Returns:
            Optional[LearnedWord]: Matching LearnedWord record if found,
            otherwise, None.
        """
        stmt = select(LearnedWord).where(
            LearnedWord.user_id == self.user_id, LearnedWord.written == written
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_writtens(
        self,
        writtens: List[str],
    ) -> Sequence[LearnedWord]:
        """
        Retrieve LearnedWord records by many writtens form.

        Args:
            writtens (List[str]): Written forms of the words.

        Returns:
            Sequence[LearnedWord]: Matching LearnedWord records if found
        """
        if len(writtens) == 0:
            return []

        stmt = select(LearnedWord).where(
            LearnedWord.user_id == self.user_id, LearnedWord.written.in_(writtens)
        )
        result = await self.session.execute(stmt)
        words = result.scalars().all()

        return words

    async def get_all(self) -> Sequence[LearnedWord]:
        """
        Retrieve all LearnedWord records marked as learned for the user.

        Returns:
            Sequence[LearnedWord]: Learned words.
        """
        stmt = select(LearnedWord).where(
            LearnedWord.user_id == self.user_id, LearnedWord.learned
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_since(self, since: datetime) -> Sequence[LearnedWord]:
        """
        Retrieve all LearnedWord records updated on or after the specified datetime.

        Args:
            since (datetime): Datetime to start the search from.

        Returns:
            Sequence[LearnedWord]: LearnedWord records updated since the given datetime.
        """
        stmt = select(LearnedWord).where(
            LearnedWord.user_id == self.user_id, LearnedWord.updated_at >= since
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_learned(self, word: LearnedWordSchema) -> LearnedWord:
        """
        Add a new LearnedWord record to the user's vocabulary.

        Args:
            word (LearnedWordSchema): Data schema containing the learned word details.

        Returns:
            LearnedWord: Newly created LearnedWord record.
        """
        learned_word = LearnedWord(
            written=word.written,
            learned=word.learned,
            updated_at=word.updated_at,
            user_id=self.user_id,
        )
        self.session.add(learned_word)
        await self.session.commit()
        return learned_word

    async def add_learned_batch(self, words: List[LearnedWordSchema]) -> LearnedWord:
        """
        Add a new LearnedWord record to the user's vocabulary.

        Args:
            word (List[LearnedWordSchema]): Data schema containing the learned words details.

        Returns:
            LearnedWord: Newly created LearnedWord record.
        """
        for word in words:
            learned_word = LearnedWord(
                written=word.written,
                learned=word.learned,
                updated_at=word.updated_at,
                user_id=self.user_id,
            )
            self.session.add(learned_word)
        await self.session.commit()
        return learned_word

    async def remove_learned(self, word: LearnedWord) -> None:
        """
        Remove an existing LearnedWord record from the user's vocabulary.

        Args:
            word (LearnedWord): LearnedWord record to remove.
        """
        await self.session.delete(word)
        await self.session.commit()

    async def get_last_update_at(self) -> Optional[datetime]:
        """
        Retrieve the timestamp of the most recent update among LearnedWord records.

        Returns:
            Optional[datetime]: Last update timestamp if available; otherwise, None.
        """
        stmt = (
            select(LearnedWord)
            .where(LearnedWord.user_id == self.user_id)
            .order_by(LearnedWord.updated_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        word = result.scalars().first()
        return word.updated_at if word else None

    async def get_count(self) -> int:
        """
        Count the number of LearnedWord records marked as learned for the user.

        Returns:
            int: Count of learned words.
        """
        stmt = select(functions.count()).where(
            LearnedWord.user_id == self.user_id, LearnedWord.learned
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() or 0

    async def get_status(self) -> VocStatusSchema:
        """
        Retrieve the user's vocabulary status.

        Returns:
            VocStatusSchema: Schema containing vocabulary status details.
        """
        learned_count = await self.get_count()
        if learned_count != 0:
            last_update_at = await self.get_last_update_at()
        else:
            last_update_at = datetime.fromtimestamp(0)
        return VocStatusSchema(learned_count=learned_count, last_update=last_update_at)

    async def clear_all(self) -> None:
        """
        Delete all learned vocabulary words for the user.
        """
        stmt = delete(LearnedWord).where(LearnedWord.user_id == self.user_id)
        await self.session.execute(stmt)
