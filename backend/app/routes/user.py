import jwt
import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.main_db import get_session
from app.models import User
from app.repository import UserRepository

# Create API root router
router = APIRouter(prefix="/user", tags=["User"])

security = HTTPBearer()


async def get_current_user_from_apple(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials
    idinfo = verify_apple_token(token)
    apple_id = idinfo.get("sub")
    if not apple_id:
        raise HTTPException(status_code=401, detail="Apple ID manquant dans le token")
    
    repository = UserRepository(session)
    user = await repository.get_by_apple_id(apple_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    return user

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials
    idinfo = verify_google_token(token)

    google_id = idinfo.get("sub")
    if not google_id:
        raise HTTPException(status_code=401, detail="Google ID manquant dans le token")

    repository = UserRepository(session)
    user = await repository.get_by_google_id(google_id)

    return user


@router.post("/learned/{word}")
async def add_learned_word(
    word: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    learned_word = LearnedWord(word=word, user_id=current_user.id)
    await session.add(learned_word)
    await session.commit()
