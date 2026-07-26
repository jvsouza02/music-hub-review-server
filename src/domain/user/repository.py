from typing import Protocol
from uuid import UUID
from .entity import User

class IUserRepository(Protocol):
    async def save(self, user: User) -> User:
        ...

    async def get_by_id(self, id: UUID) -> User | None:
        ...

    async def get_by_email(self, email: str) -> User | None:
        ...