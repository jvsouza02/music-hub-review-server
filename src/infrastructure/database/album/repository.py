from src.domain.album.repository import IAlbumRepository
from src.domain.album.entity import Album
from src.infrastructure.database.album.mapper import AlbumMapper
from src.infrastructure.database.album.model import AlbumModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from sqlalchemy import select, update, delete
from uuid import UUID
from typing import Any

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


    async def update(self, album_id: UUID, data: list[str, Any]) -> Album | None:
            if data is None:
                return None
    
            statement = (
                update(AlbumModel)
                .where(AlbumModel.id == album_id)
                .values(
                    average_score=data.get("average_score"),
                    review_count=data.get("review_count")
                )
                .returning(AlbumModel)
            )
    
            result = await self._session.execute(statement)
            await self._session.commit()
    
            updated_data = result.scalar_one_or_none()
    
            if updated_data is None:
                return None
    
            return AlbumMapper.to_entity(updated_data)
    

    async def delete(self, album_id: UUID) -> bool:
        statement = (
            delete(AlbumModel)
            .where(AlbumModel.id == album_id)
            .returning(AlbumModel)
        )

        result = self._session.execute(statement)
        await self._session.commit()

        return result.rowcount > 0