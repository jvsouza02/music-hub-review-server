from uuid import UUID
from .entity import User
from abc import ABC, abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> User | None:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def get_all(self) -> list[User] | None:
        ...

    @abstractmethod
    async def update(self, user_id: UUID, user: User) -> User | None:
        ...


    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        ...