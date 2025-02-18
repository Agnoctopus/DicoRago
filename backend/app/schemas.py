"""
Pydantic schemas for requests and responses.
"""

from typing import List, Optional

from pydantic import BaseModel


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


class AnalyseRequestSchema(BaseModel):
    """
    Schema representing an analysis request.

    Attributes:
        text (str): Text to be analyzed.
    """

    text: str


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
        english_word (str): English form.
        english_definition (str): English definition.
    """

    id: int
    english_word: str
    english_definition: str

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

    class Config:
        """
        Configuration for the WordWithSensesSchema class.
        """

        from_attributes = True
