from uuid import UUID
from .entity import Artist
from abc import ABC, abstractmethod

class IArtistRepository(ABC):
    @abstractmethod
    async def save(self, user: Artist) -> Artist:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Artist | None:
        ...

    @abstractmethod
    async def get_all(self) -> list[Artist] | None:
        ...

    @abstractmethod
    async def update(self, artist_id: UUID, artist: Artist) -> Artist | None:
        ...

    @abstractmethod
    async def delete(self, artist_id: UUID) -> bool:
        ...