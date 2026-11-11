from fastapi import APIRouter, status, Depends, Query
from .deps import get_album_service
from .schema import AlbumResponse, AlbumFiltersParams
from src.application.album.services import AlbumService
from src.application.track.services import TrackService
from src.domain.track.entity import Track
from src.presentation.api.v1.track.schema import TrackResponse
from src.presentation.api.v1.track.deps import get_track_service
from src.domain.album.entity import Album
from typing import Annotated
from uuid import UUID


album_router = APIRouter(prefix="/albums", tags=["Album"])


@album_router.get(
    "/id/{album_id}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getAlbumById"
)
async def get_album_by_id(
    album_service: Annotated[AlbumService, Depends(get_album_service)],
    album_id: UUID
) -> Album:
    return await album_service.get_album_by_id(album_id)


@album_router.get(
    "/mbid/{album_mbid}",
    response_model=AlbumResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getAlbumByMbid"
)
async def get_album_by_mbid(
    album_service: Annotated[AlbumService, Depends(get_album_service)],
    album_mbid: UUID
) -> Album:
    return await album_service.get_album_by_mbid(album_mbid)


@album_router.get(
    "/",
    response_model=list[AlbumResponse],
    operation_id="listAlbums"
)
async def get_all_albums(
    album_service: Annotated[AlbumService, Depends(get_album_service)],
    filters: Annotated[AlbumFiltersParams, Query()]
) -> list[Album]:
    return await album_service.get_all_albums(filters.limit, filters.offset)


@album_router.get(
    "/{album_id}/tracks",
    response_model=list[TrackResponse],
    status_code=status.HTTP_200_OK,
    operation_id="listAlbumTracks"
)
async def get_tracks_by_album(
    track_service: Annotated[TrackService, Depends(get_track_service)],
    album_id: UUID
) -> list[Track]:
    return await track_service.get_track_by_album(album_id)
