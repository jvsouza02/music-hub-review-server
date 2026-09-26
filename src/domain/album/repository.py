from abc import abstractmethod, ABC
from src.domain.album.entity import Album
from uuid import UUID

class IAlbumRepository(ABC):
    @abstractmethod
    async def save(self, album: Album) -> Album:
        ...

    @abstractmethod
    async def get_by_id(self, album_id: UUID) -> Album | None:
        ...

    @abstractmethod
    async def get_by_mbid(self, mbid: str) -> Album | None:
        ...