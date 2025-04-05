from datetime import datetime
from typing import List

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.databases.main_db import get_session
from app.models import User
from app.repository import UserRepository, VocRepository
from app.schemas import UserInfoSchema, VocabWordSchema, VocStatusSchema

router = APIRouter(prefix="/user", tags=["User"])


async def get_current_user(
    auth_session: str = Cookie(None),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Retrieve the current user from the session token.

    Args:
        auth_session (str): Session token from cookie.
        session (AsyncSession): DB session dependency.

    Returns:
        User: Authenticated user

    Raises:
        HTTPException: If authentication fails or user is not found.
    """
    # Verify the session cookie exists
    if auth_session is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        # Decode the JWT token using the secret key
        token = jwt.decode(auth_session, settings.AUTH_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid session token")

    # Ensure the token contains only one user identifier
    if "google_id" in token and "apple_id" in token:
        raise HTTPException(status_code=401, detail="Two user ids found in token")

    # Create repository instance to access user data
    repository = UserRepository(session)

    user = None
    # Retrieve user by Google ID or Apple ID
    if "google_id" in token:
        user = await repository.get_by_google_id(token["google_id"])
    elif "apple_id" in token:
        user = await repository.get_by_apple_id(token["apple_id"])
    else:
        raise HTTPException(status_code=401, detail="No user id found in token")

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/me", response_model=UserInfoSchema)
async def get_user_info(
    user: User = Depends(get_current_user),
) -> UserInfoSchema:
    """
    Get current user information.

    Args:
        user (User): Authenticated user.

    Returns:
        UserInfoSchema: Information of the current user.
    """
    return UserInfoSchema.from_orm(user)


@router.put("/voc", response_model=VocStatusSchema)
async def update_voc(
    voc_req: VocabWordSchema,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> VocStatusSchema:
    """
    Update a vocabulary word.

    Args:
        voc_req (VocabWordSchema): Vocabulary word details to put.
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        Optional[VocStatusSchema]: Previous vocabulary status.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    # Get previous status and vocab word
    status = await repository.get_status()
    vocab_word = await repository.get_by_written(voc_req.written)

    if vocab_word is None:
        # New word: add to vocabulary
        await repository.add_word(voc_req)
        return status

    # Update existing word
    vocab_word.status = voc_req.status
    vocab_word.updated_at = voc_req.updated_at
    await session.commit()

    return status


@router.put("/voc/batch", response_model=VocStatusSchema)
async def update_voc_batch(
    voc_req: List[VocabWordSchema],
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> VocStatusSchema:
    """
    Update multiple vocabulary words at once.

    Args:
        voc_req (List[VocabWordSchema]): List of vocabulary word details to update.
        user (User): DB session dependency.
        session (AsyncSession): Database session dependency.

    Returns:
        VocStatusSchema: The previous vocabulary status.
    """
    # Create repository instance to access vocabulary data
    repository = VocRepository(session, user.id)

    # Get previous status.
    status = await repository.get_status()

    # Filter voc_req for unique entries keyed by 'written'.
    unique_voc = {word.written: word for word in voc_req}.values()
    writtens = [word.written for word in unique_voc]

    # Retrieve existing vocab words for these written forms.
    existing_vocab = await repository.get_by_writtens(writtens)
    existing_dict = {lw.written: lw for lw in existing_vocab}

    new_words = []
    # Process each unique incoming word.
    for word in unique_voc:
        if word.written not in existing_dict:
            # Word does not exist; mark it for insertion.
            new_words.append(word)
        else:
            # Update existing word.
            existing = existing_dict[word.written]
            existing.status = word.status
            existing.updated_at = word.updated_at

    # Add new words in batch if any.
    if new_words:
        await repository.add_words(new_words)

    await session.commit()
    return status


@router.get("/voc", response_model=List[VocabWordSchema])
async def get_voc(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[VocabWordSchema]:
    """
    Retrieve all learned or seen vocabulary words.

    Args:
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        List[VocabWordSchema]: A list of learned or seen vocabulary words.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    vocab_words = await repository.get_all(["learned", "seen", "ignore"])

    return [VocabWordSchema.from_orm(word) for word in vocab_words]


@router.get("/voc/change/{since}", response_model=List[VocabWordSchema])
async def get_voc_change(
    since: datetime,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[VocabWordSchema]:
    """
    Retrieve vocabulary words updated since a specified datetime.

    Args:
        since (datetime): Datetime from which to retrieve updates.
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        List[VocabWordSchema]: Vocabulary words updated since the specified datetime.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    vocab_words = await repository.get_since(since)

    return [VocabWordSchema.from_orm(word) for word in vocab_words]


@router.get("/voc/status", response_model=VocStatusSchema)
async def get_last_voc(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> VocStatusSchema:
    """
    Retrieve the vocabulary status.

    Args:
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        VocStatusSchema: The vocabulary status of the user.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    status = await repository.get_status()

    return status


@router.delete("/voc", status_code=status.HTTP_204_NO_CONTENT)
async def clear_vocabulary(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Response:
    """
    Deletes all vocabulary words for the authenticated user.

    Args:
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        Response: Responds with HTTP 204 No Content upon success.
    """
    repository = VocRepository(session, user.id)

    await repository.clear_all()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
