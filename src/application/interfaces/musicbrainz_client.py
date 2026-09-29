from abc import ABC, abstractmethod
from typing import Any


class IMusicBrainzClient(ABC):
    @abstractmethod
    async def search(
        self,
        query: str,
        entity_type: str,
        limit: int = 25,
        offset: int = 0
    ) -> list[dict[str, Any]]:
        """Busca entidades que batem com uma query de texto."""
        ...

    @abstractmethod
    async def get_artist(
        self, 
        mbid: str, 
        inc: str | None = None
    ) -> dict[str, Any] | None:
        """Busca dados de um artista pelo seu MBID."""
        ...

    @abstractmethod
    async def get_release_group(
        self, 
        mbid: str, 
        inc: str | None = None
    ) -> dict[str, Any] | None:
        """Busca dados de um grupo de lançamentos (álbum/EP) pelo seu MBID."""
        ...

    @abstractmethod
    async def get_album(
        self, 
        mbid: str, 
        inc: str | None = None
    ) -> dict[str, Any] | None:
        """Busca dados de um álbum (alias para get_release_group)."""
        ...

    @abstractmethod
    async def get_release(
        self, 
        mbid: str, 
        inc: str | None = None
    ) -> dict[str, Any] | None:
        """Busca dados de um lançamento específico pelo seu MBID."""
        ...

    @abstractmethod
    async def get_recording(
        self, 
        mbid: str, 
        inc: str | None = None
    ) -> dict[str, Any] | None:
        """Busca dados de uma gravação/faixa pelo seu MBID."""
        ...

    @abstractmethod
    async def browse_recordings_by_artist(
        self, 
        artist_mbid: str, 
        limit: int = 25, 
        offset: int = 0
    ) -> list[dict[str, Any]]:
        """Navega pelas gravações de um artista específico."""
        ...
