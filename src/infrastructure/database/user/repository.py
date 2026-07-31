from src.domain.user.repository import IUserRepository
from src.domain.user.entity import User
from src.infrastructure.database.user.model import UserModel
from src.infrastructure.database.user.mapper import UserMapper
from src.domain.user.exceptions import EmailAlreadyInUseException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import Any

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session


    async def save(self, user: User) -> User:
        user_model = UserMapper.to_model(user)

        try:
            self._session.add(user_model)
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise EmailAlreadyInUseException()

        return UserMapper.to_entity(user_model)


    async def get_by_id(self, id: UUID) -> User | None:
        statement = select(UserModel).where(UserModel.id == id)

        result = await self._session.execute(statement)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return UserMapper.to_entity(model=user_model)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        
        result = await self._session.execute(statement)
        user_model = result.scalar_one_or_none()

        if not user_model:
            return None

        return UserMapper.to_entity(model=user_model)


    async def get_all(self) -> list[User]:
        statement = select(UserModel)

        result = await self._session.execute(statement)
        users_model = result.scalars().all()

        return [UserMapper.to_entity(model=user) for user in users_model]


    async def update(
            self, user_id: UUID, update_data: dict[str, Any]
    ) -> User | None:
        if not update_data:
            return None
        
        statement = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**update_data)
            .returning(UserModel)
        )

        try:
            result = await self._session.execute(statement)
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise EmailAlreadyInUseException()

        updated_model = result.scalar_one_or_none()
        if updated_model is None:
            return None

        return UserMapper.to_entity(updated_model)


    async def delete(self, user_id: UUID) -> bool:
        statement = delete(UserModel).where(UserModel.id == user_id)

        result = await self._session.execute(statement)
        await self._session.commit()

        return result.rowcount > 0