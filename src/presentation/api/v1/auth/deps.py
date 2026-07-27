from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.application.auth.services import AuthService
from src.presentation.api.v1.user.deps import get_user_repository
from src.domain.user.entity import User
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


def get_auth_service(
        repository: Annotated[
            IUserRepository,
            Depends(get_user_repository)
        ]
) -> AuthService:
    return AuthService(repository)