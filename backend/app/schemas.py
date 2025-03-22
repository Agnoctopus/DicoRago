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
    language: Optional[str] = Field(default="en_US")

    @validator("language", pre=True, always=True)
    def check_language(cls, value):
        if value is None or value not in LANGUAGES_SUPPORTED:
            return "en_US"
        return value


class MonSchema(BaseModel):
    obligatoire: str
    optionnel: Optional[str] = Field(default="valeur_par_defaut")
    language: Optional[str] = Field(default="en_US")  # Valeur par défaut

    @validator("language", pre=True, always=True)
    def check_language(cls, value):
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


class LearnedWordSchema(BaseModel):
    """
    Schema representing a learned word.

    Attributes:
        written (str): Written form.
        learned (bool): Whether the word is learned.
        updated_at (datetime): Timestamp of the last update.
    """

    written: str
    learned: bool
    updated_at: datetime

    class Config:
        """
        Configuration for the LearnedWord class.
        """

        from_attributes = True


class VocStatusSchema(BaseModel):
    """
    Represents the vocabulary status

    Attributes:
        learned_count (int): Total number of words learned.
        last_update (datetime): Timestamp of the most recent voc update.
    """

    learned_count: int
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
