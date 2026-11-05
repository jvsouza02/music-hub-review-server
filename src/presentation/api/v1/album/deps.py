from src.application.album.services import AlbumService
from src.infrastructure.database.album.repository import AlbumRepository
from src.infrastructure.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends


def get_album_service(
        session: Annotated[AsyncSession, Depends(get_db)]
):
    album_repository = AlbumRepository(session)
    return AlbumService(album_repository)