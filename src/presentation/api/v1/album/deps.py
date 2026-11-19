from src.application.album.services import AlbumService
from src.infrastructure.database.album.repository import AlbumRepository
from src.infrastructure.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from src.infrastructure.external.musicbrainz.client import MusicBrainzClient
from src.core.config import settings


def get_album_service(
        session: Annotated[AsyncSession, Depends(get_db)]
):
    album_repository = AlbumRepository(session)
    mbz_client = MusicBrainzClient(
        app_name=settings.PROJECT_NAME,
        app_version=settings.VERSION,
       contact_email=settings.ADMIN_EMAIL
    )

    return AlbumService(album_repository, mbz_client)