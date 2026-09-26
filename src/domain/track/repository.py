from src.domain.track.entity import Track
from abc import abstractmethod, ABC
from uuid import UUID

class ITrackRepository(ABC):
    @abstractmethod
    async def save(self, track: Track) -> Track:
        ...

    @abstractmethod
    async def get_by_id(self, track_id: UUID) -> Track | None:
        ...

    @abstractmethod
    async def get_by_mbid(self, mbid: str) -> Track | None:
        ...

    @abstractmethod
    async def get_by_album(self, album_id: UUID) -> list[Track]:
        ...