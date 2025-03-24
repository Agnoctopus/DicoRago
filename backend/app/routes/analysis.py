"""
Application API routes module.

Endpoints:
- POST /analyze: Analyze Korean.
- GET /senses/{sense_id}/examples: Retrieve examples for a given sense.
- GET /words/{word_id}/senses: Retrieve senses for a given word.
- GET /words/{word_id}: Retrieve a word by its identifier.
- GET /written/{written}/words: Retrieve words by their written form.
"""

from typing import List, Union

import khaiii
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.analyse import get_vocabulary
from app.databases.dict_db import SessionLocal, get_session
from app.models import Word
from app.repository import ExampleRepository, SenseRepository, WordRepository
from app.schemas import (
    AnalyseRequestSchema,
    AnalysisSchema,
    ExampleSchema,
    MorphSchema,
    SenseSchema,
    UnitSchema,
    WordSchema,
    WordWithSensesSchema,
)

# Create API root router
router = APIRouter(prefix="", tags=["Analysis"])


def convert_word_to_schema(word: Word) -> WordWithSensesSchema:
    """
    Converts a single Word object into a WordWithSensesSchema object.

    Args:
        word (Word): The Word object to convert.

    Returns:
        WordWithSensesSchema: The converted WordWithSensesSchema object.
    """
    return WordWithSensesSchema(
        id=word.id,
        written=word.written,
        category=word.category,
        senses=[
            SenseSchema(
                id=sense.id,
                translation=sense.translations[0].written,
                definition=sense.translations[0].definition,
            )
            for sense in word.senses
            if sense.translations
        ],
    )


def convert_words_to_schema(words: List[Word]) -> List[WordWithSensesSchema]:
    """
    Converts a list of Word objects into a list of WordWithSensesSchema objects,
    using the convert_word_to_schema helper function.

    Args:
        words (List[Word]): A list of Word objects to convert.

    Returns:
        List[WordWithSensesSchema]: A list of converted WordWithSensesSchema objects.
    """
    return [convert_word_to_schema(word) for word in words]


@router.post("/analyze", response_model=AnalysisSchema)
async def analyze_text(request: AnalyseRequestSchema) -> AnalysisSchema:
    """
    Analyze Korean text: morphological segmentation and vocabulary.

    Args:
        request (AnalyseRequestSchema): Request containing the text.

    Returns:
        AnalysisSchema: Analysis result.
    """
    # Get text
    text = request.text.strip()

    # Skip analyzing if empty text
    if len(text) == 0:
        return AnalysisSchema(units=[], vocab=[])
    # Max length limit
    if len(text) > 1000:
        return AnalysisSchema(units=[], vocab=[])

    # Create khaiii handle
    api = khaiii.KhaiiiApi()

    # Analyze the text
    try:
        analysis = api.analyze(text)
    except Exception as exception:
        raise HTTPException(
            status_code=500, detail=f"Error while analysing text: {type(exception)}"
        ) from exception

    # Construct the analysis units and vocabulary entries
    units = []
    vocs = []

    # Loop through analyzed words
    for word in analysis:
        # Reconstruct the surface form from its morphemes
        surface = "".join([m.lex for m in word.morphs])

        # Encode morphs
        morphs = [MorphSchema(lex=morph.lex, tag=morph.tag) for morph in word.morphs]

        # Get dictionary entry
        try:
            vocabulary = get_vocabulary(word)
            if vocabulary is not None:
                vocs.append(vocabulary)
        except (AssertionError, ValueError) as _:
            print(f"Error in parsing of {word}.")
            vocabulary = None

        # Craft and add unit
        unit = UnitSchema(
            surface=surface, morphs=morphs, word=word.lex, vocabulary=vocabulary
        )
        units.append(unit)

    async with SessionLocal() as session:
        repository = WordRepository(session)
        words = await repository.get_by_writtens(
            list(dict.fromkeys(vocs)), senses=True, language=request.language
        )

        vocab = convert_words_to_schema(words)
    return AnalysisSchema(units=units, vocab=vocab)


@router.get("/senses/{sense_id}/examples", response_model=List[ExampleSchema])
async def get_sense_examples(
    sense_id: int, session: AsyncSession = Depends(get_session)
) -> List[ExampleSchema]:
    """
    Retrieve examples for a given sense.

    Args:
        sense_id (int): Sense unique identifier.
        session (AsyncSession): Database session dependency.

    Returns:
        List[ExampleSchema]: Associated examples.
    """
    repository = ExampleRepository(session)
    examples = await repository.get_by_sense_id(sense_id)
    return [ExampleSchema.from_orm(example) for example in examples]


@router.get("/words/{word_id}/senses", response_model=List[SenseSchema])
async def get_word_senses(
    word_id: int, language: str = "en_US", session: AsyncSession = Depends(get_session)
) -> List[SenseSchema]:
    """
    Retrieve senses for a given word.

    Args:
        word_id (int): Word unique identifier.
        session (AsyncSession): Database session dependency.
        language (str): Language code to for translation.

    Returns:
        List[SenseSchema]: Associated senses.
    """
    repository = SenseRepository(session)
    senses = await repository.get_by_word_id(word_id, language=language)
    return [SenseSchema.from_orm(sense) for sense in senses]


@router.get("/words/{word_id}", response_model=Union[WordSchema | WordWithSensesSchema])
async def get_word(
    word_id: int,
    senses: bool = False,
    language: str = "en_US",
    session: AsyncSession = Depends(get_session),
) -> Union[WordSchema | WordWithSensesSchema]:
    """
    Retrieve a word by its unique identifier, optionally including its
    associated senses.

    Args:
        word_id (int): Word unique identifier.
        senses (bool): If True, include senses.
        language (str): Language code to for translation.
        session (AsyncSession): Database session dependency.

    Returns:
        Union[WordSchema | WordWithSensesSchema]: Corresponding word optionally
        with associated senses.
    """
    repository = WordRepository(session)
    word = await repository.get_by_id(word_id, senses=senses, language=language)
    if senses:
        return convert_word_to_schema(word)
    return WordSchema.from_orm(word)


@router.get(
    "/written/{written}/words",
    response_model=List[Union[WordSchema, WordWithSensesSchema]],
)
async def get_words(
    written: str,
    senses: bool = False,
    language: str = "en_US",
    session: AsyncSession = Depends(get_session),
) -> List[Union[WordSchema, WordWithSensesSchema]]:
    """
    Retrieve words by their written form, optionally including their associated senses.

    Args:
        written (str): Word written form.
        senses (bool): If True, include associated senses.
        language (str): Language code to for translation.
        session (AsyncSession): Database session dependency.

    Returns:
        List[Union[WordSchema, WordWithSensesSchema]]: Corresponding words,
        optionally with associated senses.
    """
    repository = WordRepository(session)
    words = await repository.get_by_written(written, senses=senses, language=language)
    if senses:
        return convert_words_to_schema(words)
    return [WordSchema.from_orm(word) for word in words]
