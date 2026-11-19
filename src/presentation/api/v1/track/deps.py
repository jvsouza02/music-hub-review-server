from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from src.application.track.services import TrackService
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.track.repository import TrackRepository
from src.presentation.api.v1.deps import get_musicbrainz_client


async def get_track_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    musicbrainz_client: Annotated[
        IMusicBrainzClient,
        Depends(get_musicbrainz_client),
    ],
) -> TrackService:
    track_repository = TrackRepository(session)

    return TrackService(
        track_repository,
        musicbrainz_client,
    )