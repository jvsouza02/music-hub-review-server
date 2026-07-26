from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.user.repository import UserRepository
from src.application.user.services import UserService


def get_user_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db)
    ]
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(repository)