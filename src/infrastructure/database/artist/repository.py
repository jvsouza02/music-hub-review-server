from src.domain.artist.repository import IArtistRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.infrastructure.database.artist.mapper import ArtistMapper
from src.domain.artist.entity import Artist


class ArtistRepository(IArtistRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, artist: Artist) -> Artist:
        artist_model = ArtistMapper.to_model(artist)

        self._session.add(artist_model)
        self._session.commit()

        return ArtistMapper.to_entity(artist_model)
    