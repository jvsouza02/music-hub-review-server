from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.album.services import AlbumService
from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from src.infrastructure.database.album.repository import AlbumRepository
from src.infrastructure.database.connection import get_db
from src.presentation.api.v1.deps import get_musicbrainz_client


async def get_album_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    musicbrainz_client: Annotated[
        IMusicBrainzClient,
        Depends(get_musicbrainz_client),
    ],
) -> AlbumService:
    album_repository = AlbumRepository(session)

    return AlbumService(
        album_repository,
        musicbrainz_client,
    )