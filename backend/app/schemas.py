"""
Pydantic schemas for requests and responses.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class MorphSchema(BaseModel):
    """
    Schema representing a morpheme.

    Attributes:
        lex (str): Lexeme.
        tag (str): Grammatical tag.
    """

    lex: str
    tag: str


class UnitSchema(BaseModel):
    """
    Schema representing a linguistic unit.

    Attributes:
        surface (str): Surface form.
        morphs (List[MorphSchema]): Associated morphemes.
        word (str): Word form.
        vocabulary (Optional[str]): Optional vocabulary form.
    """

    surface: str
    morphs: List[MorphSchema]
    word: str
    vocabulary: Optional[str]


class AnalysisSchema(BaseModel):
    """
    Schema representing the complete analysis result.

    Attributes:
        units (List[UnitSchema]): Analyzed units.
        vocab (List[WordWithSensesSchema]): Vocabulary from analysis.
    """

    units: List[UnitSchema]
    vocab: List["WordWithSensesSchema"]


LANGUAGES_SUPPORTED = {"en_US", "ko_KR", "fr_FR", "es_ES", "ja_JP"}


class AnalyseRequestSchema(BaseModel):
    """
    Schema representing an analysis request.

    Attributes:
        text (str): Text to be analyzed.
        language (str): Language of the dictionary.
    """

    text: str
    language: str = Field(default="en_US")

    @validator("language", pre=True, always=True)
    # pylint: disable=no-self-argument
    def check_language(cls, value: Optional[str]) -> str:
        """
        Validates the 'language' field.

        Args:
            value (Optional[str]): Language value provided by the user.

        Returns:
            str: The valid language code.
        """
        if value is None or value not in LANGUAGES_SUPPORTED:
            return "en_US"
        return value


class ExampleSchema(BaseModel):
    """
    Schema representing an example usage of a sense.

    Attributes:
        category (str): Example category.
        example (str): Example text.
    """

    category: str
    example: str

    class Config:
        """
        Configuration for the ExampleSchema class.
        """

        from_attributes = True


class SenseSchema(BaseModel):
    """
    Schema representing a sense of a word.

    Attributes:
        id (int): Unique identifier.
        translation (str): Translation written form.
        definition (str): Translation definition.
    """

    id: int
    translation: str
    definition: str

    class Config:
        """
        Configuration for the SenseSchema class.
        """

        from_attributes = True


class WordSchema(BaseModel):
    """
    Schema representing a word.

    Attributes:
        id (int): Unique identifier.
        written (str): Written form.
        category (str): Word category.
    """

    id: int
    written: str
    category: str

    class Config:
        """
        Configuration for the WordSchema class.
        """

        from_attributes = True


class WordWithSensesSchema(WordSchema):
    """
    Schema representing a word with its senses.

    Attributes:
        senses (List[SenseSchema]): Associated senses.
    """

    senses: List[SenseSchema]


class UserInfoSchema(BaseModel):
    """
    Schema representing a user.

    Attributes:
        name (str): Username.
        email (str): E-mail.
        picture (str): Link to avatar picture.
    """

    name: str
    email: str
    picture: Optional[str]

    class Config:
        """
        Configuration for the UserInfoSchema class.
        """

        from_attributes = True


class VocabWordSchema(BaseModel):
    """
    Schema representing a vocab word.

    Attributes:
        written (str): Written form.
        status (str): Status of the word.
        updated_at (datetime): Timestamp of the last update.
    """

    written: str
    status: str
    updated_at: datetime

    @validator("status")
    # pylint: disable=no-self-argument
    def validate_status(cls, value: str) -> str:
        """
        Validates the 'status' field to ensure it is one of the allowed statuses.

        Args:
            value (str): The status value provided by the user.

        Raises:
            ValueError: If the provided status is not in the allowed set.

        Returns:
            str: The validated status value.
        """
        allowed_statuses = {"unknown", "learned", "ignore", "seen"}
        if value not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return value

    class Config:
        """
        Configuration for the VocabWord class.
        """

        from_attributes = True


class VocStatusSchema(BaseModel):
    """
    Represents the vocabulary status

    Attributes:
        status_count (int): Total number of seen and learned words.
        last_update (datetime): Timestamp of the most recent voc update.
    """

    status_count: int
    last_update: datetime


class MobileInfoSchema(BaseModel):
    """
    Represents the mobile information

    Attributes:
        min_version_ios (str): Minimum version to run the app on iOS.
        min_version_android (str): Minimum version to run the app on Android.
    """

    min_version_ios: str
    min_version_android: str
