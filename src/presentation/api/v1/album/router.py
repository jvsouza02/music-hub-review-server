from fastapi import APIRouter, status, Depends
from .deps import get_album_service
from .schema import AlbumResponse, AlbumFiltersParams
from src.application.album.services import AlbumService
from src.domain.album.entity import Album
from typing import Annotated
from uuid import UUID


album_router = APIRouter(prefix="/album", tags=["Album"])


@album_router.get(
    "/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK
)
async def get_album_by_id(
    album_service: Annotated[AlbumService, Depends(get_album_service)],
    album_id: UUID
) -> Album:
    return await album_service.get_album_by_id(album_id)


@album_router.get(
    "/{album_mbid}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK
)
async def get_album_by_mbid(
    album_service: Annotated[AlbumService, Depends(get_album_service)],
    album_mbid: UUID
) -> Album:
    return await album_service.get_album_by_mbid(album_mbid)


@album_router.get(
    "/",
    response_model=list[AlbumResponse],
)
async def get_all_albums(
    album_service: Annotated[AlbumService, Depends(get_album_service)]
) -> list[Album]:
    return await album_service.get_all_albums()
