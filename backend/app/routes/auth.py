import httpx
import jwt
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.databases.main_db import get_session
from app.repository import UserRepository

router = APIRouter(prefix="/auth", tags=["Auth"])

# Auth config for Apple
APPLE_CLIENT_ID = settings.APPLE_CLIENT_ID
APPLE_CERTS_URL = "https://appleid.apple.com/auth/keys"

# Auth config for Google
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"

# Secret for signing auth session JWTs
AUTH_SECRET = settings.AUTH_SECRET


async def fetch_jwks(jwks_url: str) -> dict:
    """
    Fetch the JWKS from the given URL.

    Args:
        jwks_url (str): URL of the JWKS.

    Returns:
        dict: JSON Web Key Set.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        response.raise_for_status()
        return response.json()


def get_signing_key(certs: dict, kid: str):
    """
    Get the signing key matching the provided kid.

    Args:
        certs (dict): JWKS.
        kid (str): Key ID.

    Returns:
        Any: The signing key or None.
    """
    for jwk in certs.get("keys", []):
        if jwk.get("kid") == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
    return None


async def verify_token(token: str, jwks_url: str, audience: str, issuer: str) -> dict:
    """
    Verify a JWT using JWKS.

    Args:
        token (str): JWT token.
        jwks_url (str): JWKS URL.
        audience (str): Expected audience.
        issuer (str): Expected issuer.

    Returns:
        dict: Decoded token payload.

    Raises:
        HTTPException: For malformed, expired, or invalid tokens.
    """
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            raise HTTPException(
                status_code=401, detail="Malformed token: missing 'kid'"
            )
        certs = await fetch_jwks(jwks_url)
        key = get_signing_key(certs, kid)
        if key is None:
            raise HTTPException(status_code=401, detail="Signing key not found")
        return jwt.decode(
            token, key=key, audience=audience, issuer=issuer, algorithms=["RS256"]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def verify_google_token(token: str) -> dict:
    """
    Verify a Google JWT.

    Args:
        token (str): Google JWT.

    Returns:
        dict: Decoded payload.
    """
    return await verify_token(
        token, GOOGLE_CERTS_URL, GOOGLE_CLIENT_ID, "https://accounts.google.com"
    )


async def verify_apple_token(token: str) -> dict:
    """
    Verify an Apple JWT.

    Args:
        token (str): Apple JWT.

    Returns:
        dict: Decoded payload.
    """
    return await verify_token(
        token, APPLE_CERTS_URL, APPLE_CLIENT_ID, "https://appleid.apple.com"
    )


def create_auth_response(user_identifier: str, provider: str) -> RedirectResponse:
    """
    Create a redirect response with an auth session cookie.

    Args:
        user_identifier (str): User's unique ID.
        provider (str): "google" or "apple".

    Returns:
        RedirectResponse: Redirect to homepage with auth cookie.
    """
    token = {f"{provider}_id": user_identifier}
    auth_session = jwt.encode(token, AUTH_SECRET, algorithm="HS256")
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="auth_session",
        value=auth_session,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
    return response


@router.post("/google")
async def auth_google(
    credential: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate a user via Google.

    Args:
        credential (str): Google JWT credential.
        session (AsyncSession): DB session dependency.

    Returns:
        RedirectResponse: Redirect with auth session cookie.
    """
    idinfo = await verify_google_token(credential)
    google_id = idinfo.get("sub")
    if not google_id:
        raise HTTPException(status_code=401, detail="Google ID missing")
    repository = UserRepository(session)
    user = await repository.get_by_google_id(google_id)
    if user is None:
        email = idinfo.get("email")
        name = idinfo.get("name")
        user = await repository.create_with_google(google_id, email, name)
    return create_auth_response(google_id, "google")


@router.post("/apple")
async def auth_apple(
    id_token: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate a user via Apple.

    Args:
        id_token (str): Apple JWT id_token.
        session (AsyncSession): DB session dependency.

    Returns:
        RedirectResponse: Redirect with auth session cookie.
    """
    idinfo = await verify_apple_token(id_token)
    apple_id = idinfo.get("sub")
    if not apple_id:
        raise HTTPException(status_code=401, detail="Apple ID missing")
    repository = UserRepository(session)
    user = await repository.get_by_apple_id(apple_id)
    if user is None:
        email = idinfo.get("email")
        name = idinfo.get("name", email)
        user = await repository.create_with_apple(apple_id, email, name)
    return create_auth_response(apple_id, "apple")


@router.get("/logout")
async def logout():
    """
    Logout the user by deleting the auth session cookie.

    Returns:
        RedirectResponse: Redirect to homepage with cookie removed.
    """
    response = RedirectResponse(url="/")
    response.delete_cookie(
        key="auth_session", httponly=True, secure=True, samesite="lax"
    )
    return response
