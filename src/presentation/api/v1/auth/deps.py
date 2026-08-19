from fastapi import Depends, HTTPException, status, Path, Request
from fastapi.security import OAuth2PasswordBearer
from src.application.auth.services import AuthService
from src.application.auth.refresh_token_store import RefreshTokenStore
from src.infrastructure.cache.redis_client import RedisClient
from src.presentation.api.v1.user.deps import get_user_repository
from src.domain.user.entity import User, UserRole
from src.domain.user.exceptions import InvalidCredentialsException
from src.domain.user.repository import IUserRepository
from src.core.security import decode_token
from .constants import ACCESS_TOKEN_KEY
from typing import Annotated
import jwt
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def _extract_token(
        request: Request,
        token_header: str | None
) -> str | None:
    if token_header:
        return token_header

    cookie_token = request.cookies.get(ACCESS_TOKEN_KEY)
    if cookie_token:
        return cookie_token.replace("Bearer ", "")

    return None

async def get_current_user(
        request: Request,
        token_header: Annotated[
            str | None, 
            Depends(oauth2_scheme)
        ],
        user_repository: Annotated[
            IUserRepository,
            Depends(get_user_repository)
        ]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = _extract_token(request, token_header)
    if not token:
        raise credentials_exception

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise InvalidCredentialsException()

        user_id = UUID(payload.get("sub"))
        if not user_id:
            raise credentials_exception
    except (jwt.PyJWTError, InvalidCredentialsException, ValueError) as e:
        raise credentials_exception

    saved_user = await user_repository.get_by_id(user_id)
    if not saved_user:
        raise credentials_exception

    return saved_user


async def get_moderator_admin_user(
        current_user: Annotated[
            User,
            Depends(get_current_user)
        ]
) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied. " \
            "Admin or Moderator privileges are required."
        )

    return current_user


async def get_authorized_user(
        user_id: Annotated[UUID, Path()],
        current_user: Annotated[
            User,
            Depends(get_current_user)
        ],
) -> User:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied." \
            "You have no permission to access this route."
        )

    return current_user


def get_refresh_token_store() -> RefreshTokenStore:
    redis = RedisClient()
    return RefreshTokenStore(redis)

def get_auth_service(
        repository: Annotated[
            IUserRepository,
            Depends(get_user_repository)
        ],
        refresh_store: Annotated[
            RefreshTokenStore,
            Depends(get_refresh_token_store)
        ]
) -> "AuthService":
    return AuthService(repository, refresh_store)