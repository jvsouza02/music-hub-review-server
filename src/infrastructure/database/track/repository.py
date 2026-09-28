from src.domain.track.repository import ITrackRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.track.entity import Track
from src.infrastructure.database.track.mapper import TrackMapper
from src.infrastructure.database.track.model import TrackModel
from sqlalchemy.exc import DBAPIError
from uuid import UUID
from sqlalchemy import select

class TrackRepository(ITrackRepository):
    def __init__(self, session: AsyncSession):
        self._session = session


    async def save(self, track: Track) -> Track:
        track_model = TrackMapper.to_model(track)

        try: 
            self._session.add(track_model)
            await self._session.commit()
        except DBAPIError as error:
            await self._session.rollback()
            raise error

        return TrackMapper.to_entity(track_model)


    async def get_by_id(self, track_id: UUID) -> Track | None:
        statement = select(TrackModel).where(TrackModel.id == track_id)

        result = await self._session.execute(statement)
        track_model = result.scalar_one_or_none()

        if not track_model:
            return None

        return TrackMapper.to_entity(track_model)


    async def get_by_mbid(self, mbid: str) -> Track | None:
        statement = select(TrackModel).where(TrackModel.mbid == mbid)

        result = await self._session.execute(statement)
        track_model = result.scalar_one_or_none()

        if not track_model:
            return None

        return TrackMapper.to_entity(track_model)


    async def get_by_album(self, album_id: UUID) -> list[Track]:
        statement = select(TrackModel).where(TrackModel.album_id == album_id)

        result = await self._session.execute(statement)
        
        return [TrackMapper.to_entity(track) for track in result.scalars().all()]
        