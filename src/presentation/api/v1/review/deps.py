from fastapi import Depends
from src.infrastructure.database.connection import get_db
from src.infrastructure.database.artist.repository import ArtistRepository
from src.infrastructure.database.album.repository import AlbumRepository
from src.infrastructure.database.track.repository import TrackRepository
from src.infrastructure.database.review.repository import ReviewRepository
from src.infrastructure.external.musicbrainz import MusicBrainzClient
from src.application.review.services import ReviewService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from src.core.config import settings

async def get_review_service(
        session: Annotated[AsyncSession, Depends(get_db)]
) -> ReviewService:
    artist_repo = ArtistRepository(session)
    album_repo = AlbumRepository(session)
    track_repo = TrackRepository(session)
    review_repo = ReviewRepository(session)
    mbz_client = MusicBrainzClient(
        app_name=settings.PROJECT_NAME,
        app_version=settings.VERSION,
        contact_email=settings.ADMIN_EMAIL
    )

    return ReviewService(
        review_repository=review_repo,
        artist_repository=artist_repo,
        album_repository=album_repo,
        track_repository=track_repo,
        musicbrainz_client=mbz_client   
    )
