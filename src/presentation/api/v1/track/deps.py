from src.infrastructure.database.track.repository import TrackRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db
from typing import Annotated
from fastapi import Depends
from src.application.track.services import TrackService

async def get_track_service(
        session: Annotated[AsyncSession, Depends(get_db)]
) -> TrackService:
    track_repository = TrackRepository(session)
    return TrackService(track_repository)