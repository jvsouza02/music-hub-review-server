from src.application.artist.services import ArtistService
from src.infrastructure.database.artist.repository import ArtistRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db
from typing import Annotated

async def get_artist_service(
        session: Annotated[AsyncSession, get_db]
):
    artist_repo = ArtistRepository(session)
    return ArtistService(artist_repo)
