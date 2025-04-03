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

from app.models import Example, Sense, SenseTranslation, User, VocabWord, Word
from app.schemas import VocabWordSchema, VocStatusSchema


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
    Repository for VocabWord model.
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

    async def get_by_written(self, written: str) -> Optional[VocabWord]:
        """
        Retrieve a VocabWord record by its written form.

        Args:
            written (str): Written form of the word.

        Returns:
            Optional[VocabWord]: Matching VocabWord record if found,
            otherwise, None.
        """
        stmt = select(VocabWord).where(
            VocabWord.user_id == self.user_id, VocabWord.written == written
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_writtens(
        self,
        writtens: List[str],
    ) -> Sequence[VocabWord]:
        """
        Retrieve VocabWord records by many writtens form.

        Args:
            writtens (List[str]): Written forms of the words.

        Returns:
            Sequence[VocabWord]: Matching VocabWord records if found
        """
        if len(writtens) == 0:
            return []

        stmt = select(VocabWord).where(
            VocabWord.user_id == self.user_id, VocabWord.written.in_(writtens)
        )
        result = await self.session.execute(stmt)
        words = result.scalars().all()

        return words

    async def get_all(self, statuses: Sequence[str]) -> Sequence[VocabWord]:
        """
        Retrieve all VocabWord records whose status is in the provided list.

        Args:
            statuses (Sequence[str]): List of statuses to filter by.

        Returns:
            Sequence[VocabWord]: Matching VocabWord.
        """
        if not statuses:
            return []

        stmt = select(VocabWord).where(
            VocabWord.user_id == self.user_id, VocabWord.status.in_(statuses)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_since(self, since: datetime) -> Sequence[VocabWord]:
        """
        Retrieve all VocabWord records updated on or after the specified datetime.

        Args:
            since (datetime): Datetime to start the search from.

        Returns:
            Sequence[VocabWord]: VocabWord records updated since the given datetime.
        """
        stmt = select(VocabWord).where(
            VocabWord.user_id == self.user_id, VocabWord.updated_at >= since
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_word(self, word: VocabWordSchema) -> VocabWord:
        """
        Add a new VocabWord record to the user's vocabulary.

        Args:
            word (VocabWordSchema): Data schema containing the VocabWord details.

        Returns:
            VocabWord: Newly created VocabWord record.
        """
        vocab_word = VocabWord(
            written=word.written,
            status=word.status,
            updated_at=word.updated_at,
            user_id=self.user_id,
        )
        self.session.add(vocab_word)
        await self.session.commit()
        return vocab_word

    async def add_words(self, words: List[VocabWordSchema]) -> VocabWord:
        """
        Add a new VocabWord record to the user's vocabulary.

        Args:
            word (List[VocabWordSchema]): Data schema containing the VocabWord details.

        Returns:
            VocabWord: Newly created VocabWord records.
        """
        vocab_words = []
        for word in words:
            vocab_word = VocabWord(
                written=word.written,
                status=word.status,
                updated_at=word.updated_at,
                user_id=self.user_id,
            )
            self.session.add(vocab_word)
            vocab_words.append(vocab_word)
        await self.session.commit()
        return vocab_words

    async def remove_word(self, word: VocabWord) -> None:
        """
        Remove an existing VocabWord record from the user's vocabulary.

        Args:
            word (VocabWord): VocabWord record to remove.
        """
        await self.session.delete(word)
        await self.session.commit()

    async def get_last_update_at(self) -> Optional[datetime]:
        """
        Retrieve the timestamp of the most recent update among VocabWord records.

        Returns:
            Optional[datetime]: Last update timestamp if available; otherwise, None.
        """
        stmt = (
            select(VocabWord)
            .where(VocabWord.user_id == self.user_id)
            .order_by(VocabWord.updated_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        word = result.scalars().first()
        return word.updated_at if word else None

    async def get_count(self, statuses: Sequence[str]) -> int:
        """
        Count the number of VocabWord records filter by statues.

        Args:
            statuses (Sequence[str]): List of statuses to filter by.

        Returns:
            int: Count of words matching statuses.
        """
        if not statuses:
            return 0

        stmt = select(functions.count()).where(
            VocabWord.user_id == self.user_id, VocabWord.status.in_(statuses)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() or 0

    async def get_status(self) -> VocStatusSchema:
        """
        Retrieve the user's vocabulary status.

        Returns:
            VocStatusSchema: Schema containing vocabulary status details.
        """
        status_count = await self.get_count(["learned", "seen", "ignore"])
        if status_count != 0:
            last_update_at = await self.get_last_update_at()
        else:
            last_update_at = datetime.fromtimestamp(0)
        return VocStatusSchema(status_count=status_count, last_update=last_update_at)

    async def clear_all(self) -> None:
        """
        Delete all vocabulary words for the user.
        """
        stmt = delete(VocabWord).where(VocabWord.user_id == self.user_id)
        await self.session.execute(stmt)
