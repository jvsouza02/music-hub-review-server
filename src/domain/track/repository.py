from src.domain.track.entity import Track
from abc import abstractmethod, ABC
from uuid import UUID
from typing import Any

class ITrackRepository(ABC):
    @abstractmethod
    async def save(self, track: Track) -> Track:
        ...

    @abstractmethod
    async def get_by_id(self, track_id: UUID) -> Track | None:
        ...

    @abstractmethod
    async def get_by_id_with_album_mbid(self, track_id: UUID) -> tuple[Track, str] | None:
        ...

    @abstractmethod
    async def get_by_mbid(self, mbid: str) -> Track | None:
        ...

    @abstractmethod
    async def get_by_mbids_with_album_mbids(self, mbid: str) -> list[tuple[Track, str]]:
        ...

    @abstractmethod
    async def get_by_album(self, album_id: UUID) -> list[Track]:
        ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[Track]:
        ...

    @abstractmethod
    async def get_all_with_album_mbids(self, limit: int, offset: int) -> list[tuple[Track, str]]:
        ...

    @abstractmethod
    async def update(self, track_id: UUID, data: dict[str, Any]) -> Track | None:
        ...

    @abstractmethod
    async def delete(self, track_id: UUID) -> bool:
        ...