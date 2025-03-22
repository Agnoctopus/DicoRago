from datetime import datetime
from typing import List

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.databases.main_db import get_session
from app.models import User
from app.repository import UserRepository, VocRepository
from app.schemas import LearnedWordSchema, UserInfoSchema, VocStatusSchema

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
    voc_req: LearnedWordSchema,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> VocStatusSchema:
    """
    Put a vocabulary word.

    Args:
        voc_req (LearnedWordSchema): Vocabulary word details to put.
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        Optional[VocStatusSchema]: Previous vocabulary status.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    # Get previous status and learned word
    status = await repository.get_status()
    learned_word = await repository.get_by_written(voc_req.written)

    if learned_word is None:
        # New word: add to vocabulary
        await repository.add_learned(voc_req)
        return status

    # Update existing word
    learned_word.learned = voc_req.learned
    learned_word.updated_at = voc_req.updated_at
    await session.commit()

    return status


@router.put("/voc/batch", response_model=VocStatusSchema)
async def update_voc(
    voc_req: List[LearnedWordSchema],
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> VocStatusSchema:
    """
    Update multiple vocabulary words at once.

    This endpoint updates the learning status for multiple vocabulary words.
    It filters the input for unique 'written' values, retrieves the existing learned words,
    updates those that already exist, and adds new ones for the rest.

    Args:
        voc_req (List[LearnedWordSchema]): List of vocabulary word details to update.
        user (User): DB session dependency.
        session (AsyncSession): Database session dependency.

    Returns:
        VocStatusSchema: The previous vocabulary status.
    """
    repository = VocRepository(session, user.id)

    # Get previous status.
    status = await repository.get_status()

    # Filter voc_req for unique entries keyed by 'written'.
    unique_voc = {word.written: word for word in voc_req}.values()
    writtens = [word.written for word in unique_voc]

    # Retrieve existing learned words for these written forms.
    existing_learned = await repository.get_by_writtens(writtens)
    existing_dict = {lw.written: lw for lw in existing_learned}

    new_words = []
    # Process each unique incoming word.
    for word in unique_voc:
        if word.written not in existing_dict:
            # Word does not exist; mark it for insertion.
            new_words.append(word)
        else:
            # Update existing word.
            existing = existing_dict[word.written]
            existing.learned = word.learned
            existing.updated_at = word.updated_at

    # Add new words in batch if any.
    if new_words:
        await repository.add_learned_batch(new_words)

    await session.commit()
    return status


@router.get("/voc", response_model=List[LearnedWordSchema])
async def get_voc(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[LearnedWordSchema]:
    """
    Retrieve all learned vocabulary words.

    Args:
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        List[LearnedWordSchema]: A list of learned vocabulary words.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    learned_words = await repository.get_all()

    return [LearnedWordSchema.from_orm(word) for word in learned_words]


@router.get("/voc/change/{since}", response_model=List[LearnedWordSchema])
async def get_voc_change(
    since: datetime,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[LearnedWordSchema]:
    """
    Retrieve vocabulary words updated since a specified datetime.

    Args:
        since (datetime): Datetime from which to retrieve updates.
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        List[LearnedWordSchema]: Vocabulary words updated since the specified datetime.
    """
    # Create repository instance to access user data
    repository = VocRepository(session, user.id)

    learned_words = await repository.get_since(since)

    return [LearnedWordSchema.from_orm(word) for word in learned_words]


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
) -> None:
    """
    Deletes all learned vocabulary words for the authenticated user.

    Args:
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        None: Responds with HTTP 204 No Content upon success.
    """
    repository = VocRepository(session, user.id)

    await repository.clear_all()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
