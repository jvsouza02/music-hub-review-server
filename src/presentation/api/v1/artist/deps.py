from src.application.artist.services import ArtistService
from src.infrastructure.database.artist.repository import ArtistRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db
from src.infrastructure.external.musicbrainz.client import MusicBrainzClient
from src.core.config import settings
from typing import Annotated
from fastapi import Depends

async def get_artist_service(
        session: Annotated[AsyncSession, Depends(get_db)]
):
    artist_repo = ArtistRepository(session)
    mbz_client = MusicBrainzClient(
        app_name=settings.PROJECT_NAME,
        app_version=settings.VERSION,
        contact_email=settings.ADMIN_EMAIL
    )

    return ArtistService(artist_repo, mbz_client)
