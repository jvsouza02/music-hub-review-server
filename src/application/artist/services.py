from src.domain.artist.entity import Artist
from src.domain.artist.exceptions import ArtistNotFoundException
from src.domain.artist.repository import IArtistRepository
from uuid import UUID

class ArtistService:
    def __init__(self, artist_repository: IArtistRepository):
        self._artist_repository = artist_repository


    async def get_artist_by_id(self, artist_id: UUID) -> Artist:
        artist = await self._artist_repository.get_by_id(artist_id)

        if artist is None:
            raise ArtistNotFoundException()

        return artist


    async def get_artist_by_mbid(self, artist_mbid: str) -> Artist:
        artist = await self._artist_repository.get_by_mbid(artist_mbid)

        if artist is None:
            raise ArtistNotFoundException()

        return artist


    async def get_all_artist(self, limit: int, offset = 0) -> list[Artist]:
        return await self._artist_repository.get_all(limit, offset)

