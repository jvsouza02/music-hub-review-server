from src.domain.user.repository import IUserRepository
from src.domain.user.entity import User
from src.infrastructure.database.user.model import UserModel
from src.infrastructure.database.user.mapper import UserMapper
from src.domain.user.exceptions import EmailAlreadyInUseException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session


    async def save(self, user: User) -> User:
        user_model = UserMapper.to_model(user)

        try:
            self._session.add(user_model)
            await self._session.commit()
        except IntegrityError as e:
            await self._session.rollback()
            raise EmailAlreadyInUseException("Este e-mail já está em uso.")

        return UserMapper.to_entity(user_model)


    async def get_by_id(self, id: UUID) -> User | None:
        ...

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        
        result = await self._session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return UserMapper.to_entity(model=user_model)