from src.domain.artist.repository import IArtistRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.database.artist.mapper import ArtistMapper
from src.infrastructure.database.artist.model import ArtistModel
from src.domain.artist.entity import Artist
from sqlalchemy.exc import DBAPIError
from uuid import UUID


class ArtistRepository(IArtistRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, artist: Artist) -> Artist:
        artist_model = ArtistMapper.to_model(artist)

        try:
            self._session.add(artist_model)
            await self._session.commit()
        except DBAPIError as error:
            await self._session.rollback()
            raise error

        return ArtistMapper.to_entity(artist_model)


    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        statement = select(ArtistModel).where(ArtistModel.id == artist_id)

        result = await self._session.execute(statement)
        artist_model = result.scalar_one_or_none()

        if artist_model is None:
            return None

        return ArtistMapper.to_entity(artist_model)


    async def get_by_mbid(self, artist_mbid: str) -> Artist | None:
        statement = select(ArtistModel).where(ArtistModel.mbid == artist_mbid)

        result = await self._session.execute(statement)
        artist_model = result.scalar_one_or_none()

        if artist_model is None:
            return None

        return ArtistMapper.to_entity(artist_model)    