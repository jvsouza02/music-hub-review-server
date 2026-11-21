from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from src.application.review.services import ReviewService
from src.infrastructure.database.artist.repository import ArtistRepository
from src.infrastructure.database.album.repository import AlbumRepository
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.review.repository import ReviewRepository
from src.infrastructure.database.track.repository import TrackRepository
from src.presentation.api.v1.deps import get_musicbrainz_client


async def get_review_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    musicbrainz_client: Annotated[
        IMusicBrainzClient,
        Depends(get_musicbrainz_client),
    ],
) -> ReviewService:
    artist_repo = ArtistRepository(session)
    album_repo = AlbumRepository(session)
    track_repo = TrackRepository(session)
    review_repo = ReviewRepository(session)

    return ReviewService(
        review_repository=review_repo,
        artist_repository=artist_repo,
        album_repository=album_repo,
        track_repository=track_repo,
        musicbrainz_client=musicbrainz_client,
    )