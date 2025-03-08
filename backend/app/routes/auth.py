"""
Application API routes module.

Endpoints:
- ...
"""

import jwt
import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.databases.main_db import get_session
from app.repository import UserRepository
from app.routes.user import get_current_user

# Create API root router
router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()

# Apple auth params
APPLE_CLIENT_ID = settings.APPLE_CLIENT_ID
APPLE_CERTS_URL = "https://appleid.apple.com/auth/keys"

# Google auth params
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"


def verify_google_token(token: str):
    try:
        # Récupération de l'en-tête non vérifié pour extraire le kid (identifiant de la clé)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Token mal formé")

        # Récupération des clés publiques de Google
        response = requests.get(GOOGLE_CERTS_URL)
        response.raise_for_status()
        certs = response.json()

        # Sélection de la clé correspondant au kid du token
        key = None
        for jwk in certs.get("keys", []):
            if jwk.get("kid") == kid:
                key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
                break

        if key is None:
            raise HTTPException(status_code=401, detail="Clé introuvable pour le token")

        # Décodage et vérification du token
        idinfo = jwt.decode(
            token, key=key, audience=GOOGLE_CLIENT_ID, algorithms=["RS256"]
        )
        return idinfo

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


@router.post("/google")
async def auth_google(
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
    if user is None:
        email = idinfo.get("email")
        name = idinfo.get("name")

        user = await repository.create(google_id, email, name)

    return {"user": idinfo}



def verify_apple_token(token: str):
    try:
        # Extraction de l'en-tête pour récupérer le kid
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Token mal formé : 'kid' manquant")

        # Récupération des clés publiques d'Apple
        response = requests.get(APPLE_CERTS_URL)
        response.raise_for_status()
        certs = response.json()

        # Sélection de la clé correspondant au kid
        key = None
        for jwk in certs.get("keys", []):
            if jwk.get("kid") == kid:
                key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
                break

        if key is None:
            raise HTTPException(status_code=401, detail="Clé introuvable pour le token")

        # Décodage et vérification du token avec RS256
        payload = jwt.decode(
            token,
            key=key,
            audience=APPLE_CLIENT_ID,
            issuer="https://appleid.apple.com",
            algorithms=["RS256"]
        )
        return payload

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

@router.post("/apple")
async def auth_apple(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    token = credentials.credentials
    idinfo = verify_apple_token(token)

    print(idinfo)
    return
    # Récupération d'un identifiant unique (Apple utilise "sub")
    apple_id = idinfo.get("sub")
    if not apple_id:
        raise HTTPException(status_code=401, detail="Apple ID manquant dans le token")

    repository = UserRepository(session)
    user = await repository.get_by_apple_id(apple_id)  # Méthode à implémenter dans votre repo

    if user is None:
        email = idinfo.get("email")
        name = idinfo.get("name")  # Notez que name n'est retourné qu'à la première connexion
        user = await repository.create_apple_user(apple_id, email, name)

    return {"user": idinfo}