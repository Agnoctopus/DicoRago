import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.databases.main_db import get_session
from app.models import LearnedWord, User
from app.repository import UserRepository
from app.schemas import UserInfoSchema

router = APIRouter(prefix="/user", tags=["User"])


async def get_current_user(
    auth_session: str = Cookie(None),
    session: AsyncSession = Depends(get_session),
):
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

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/me", response_model=UserInfoSchema)
async def get_user_info(
    user: User = Depends(get_current_user),
):
    """
    Get current user information.

    Args:
        user (User): Authenticated user.

    Returns:
        UserInfoSchema: Information of the current user.
    """
    return user


@router.post("/learned/{word}")
async def add_learned_word(
    word: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Add a learned word for the current user.

    Args:
        word (str): Word to be added as learned.
        user (User): Authenticated user.
        session (AsyncSession): DB session dependency.

    Returns:
        None
    """
    # Create a nd Add a LearnedWord object
    learned_word = LearnedWord(word=word, user_id=user.id)
    await session.add(learned_word)
    await session.commit()
