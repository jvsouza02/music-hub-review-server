# importar entidade, interface de repositorio, exceptions e security para gerar senha hash
from src.core.security import generate_password_hash
from src.domain.user.entity import User
from src.domain.user.exceptions import UserNotFoundException
from src.domain.user.repository import IUserRepository
from uuid import UUID

class UserService:
    def __init__(self, repository: IUserRepository):
        self._user_repository = repository

    async def create_user(self, username: str, email: str, password: str) -> User:
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
        )

        saved_user = await self._user_repository.save(new_user)

        return saved_user


    async def get_user(self, user_id: UUID) -> User:
        saved_user = await self._user_repository.get_by_id(user_id)

        if saved_user is None:
            raise UserNotFoundException()

        return saved_user


    async def get_users(self) -> list[User]:
        return await self._user_repository.get_all()
    

    async def edit_user(self, user_id: UUID, **update_data) -> User:
        if "password" in update_data and update_data["password"]:
            update_data["password"] = generate_password_hash(update_data["password"])

        updated_user = await self._user_repository.update(user_id, update_data)

        if not updated_user:
            raise UserNotFoundException()

        return updated_user


    async def delete_user(self, user_id: UUID) -> None:
        is_deleted = await self._user_repository.delete(user_id)

        if not is_deleted:
            raise UserNotFoundException()

        return None

