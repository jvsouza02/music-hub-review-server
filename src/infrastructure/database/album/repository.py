from src.domain.album.repository import IAlbumRepository
from src.domain.album.entity import Album
from src.infrastructure.database.album.mapper import AlbumMapper
from src.infrastructure.database.album.model import AlbumModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from sqlalchemy import select
from uuid import UUID

class AlbumRepository(IAlbumRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, album: Album) -> Album:
        album_model = AlbumMapper.to_model(album)

        try:
            self._session.add(album_model)
            await self._session.commit()
        except DBAPIError as error:
            await self._session.rollback()
            raise error

        return AlbumMapper.to_entity(album_model)


    async def get_by_id(self, album_id: UUID) -> Album | None:
        statement = select(AlbumModel).where(AlbumModel.id == album_id)

        result = await self._session.execute(statement)
        album_model = result.scalar_one_or_none()

        if not album_model:
            return None

        return AlbumMapper.to_entity(album_model)


    async def get_by_mbid(self, mbid: str) -> Album | None:
        statement = select(AlbumModel).where(AlbumModel.mbid == mbid)

        result = await self._session.execute(statement)
        album_model = result.scalar_one_or_none()

        if not album_model:
            return None

        return AlbumMapper.to_entity(album_model)
    
    
        