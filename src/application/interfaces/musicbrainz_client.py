from abc import ABC, abstractmethod
from typing import Any

class  IMusicBrainzClient(ABC):
    @abstractmethod
    async def search(
        self, query: str, entity_type: str
    ) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def get_artist(self, mbid: str) -> dict[str, Any] | None:
        ...

    @abstractmethod
    async def get_album(self, mbid: str) -> dict[str, Any] | None:
        ...

    @abstractmethod
    async def get_track(self, mbid: str) -> dict[str, Any] | None:
        ...