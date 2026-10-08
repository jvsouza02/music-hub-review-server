from uuid import UUID
from .entity import Artist
from abc import ABC, abstractmethod
from typing import Any

class IArtistRepository(ABC):
    @abstractmethod
    async def save(self, artist: Artist) -> Artist:
        ...

    @abstractmethod
    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        ...

    @abstractmethod
    async def get_by_mbid(self, artist_mbid: str) -> Artist | None:
        ...

    # @abstractmethod
    # async def get_all(self) -> list[Artist] | None:
    #     ...

    @abstractmethod
    async def update(self, artist_id: UUID, data: dict[str, Any]) -> Artist | None:
        ...

    @abstractmethod
    async def delete(self, artist_id: UUID) -> bool:
        ...