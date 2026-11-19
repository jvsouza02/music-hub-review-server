from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.artist.services import ArtistService
from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from src.infrastructure.database.artist.repository import ArtistRepository
from src.infrastructure.database.connection import get_db
from src.presentation.api.v1.deps import get_musicbrainz_client


async def get_artist_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    musicbrainz_client: Annotated[
        IMusicBrainzClient,
        Depends(get_musicbrainz_client),
    ],
) -> ArtistService:
    artist_repository = ArtistRepository(session)

    return ArtistService(
        artist_repository,
        musicbrainz_client,
    )