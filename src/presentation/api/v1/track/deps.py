from src.infrastructure.database.track.repository import TrackRepository
from src.infrastructure.external.musicbrainz.client import MusicBrainzClient
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db
from typing import Annotated
from fastapi import Depends
from src.application.track.services import TrackService

async def get_track_service(
        session: Annotated[AsyncSession, Depends(get_db)]
) -> TrackService:
    track_repository = TrackRepository(session)
    mbz_client = MusicBrainzClient(
        app_name=settings.PROJECT_NAME,
        app_version=settings.VERSION,
        contact_email=settings.ADMIN_EMAIL
        )
    return TrackService(track_repository, mbz_client)