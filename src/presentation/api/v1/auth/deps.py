from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from src.application.auth.services import AuthService
from src.presentation.api.v1.user.deps import get_user_repository
from src.domain.user.entity import User, UserRole
from src.domain.user.repository import IUserRepository
from src.core.config import settings
from typing import Annotated
import jwt
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
        token: Annotated[
            str, 
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

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    
    except jwt.PyJWTError:
        raise credentials_exception

    saved_user = await user_repository.get_by_id(UUID(user_id))
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


def get_auth_service(
        repository: Annotated[
            IUserRepository,
            Depends(get_user_repository)
        ]
) -> AuthService:
    return AuthService(repository)