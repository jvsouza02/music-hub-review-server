from .deps import get_artist_service
from src.application.artist.services import ArtistService
from src.application.album.services import AlbumService
from src.domain.artist.entity import Artist
from fastapi import APIRouter, status, Depends
from .schema import ArtistResponse, ArtistFiltersParams
from src.presentation.api.v1.album.schema import AlbumResponse
from src.presentation.api.v1.album.deps import get_album_service
from src.domain.album.entity import Album
from typing import Annotated
from uuid import UUID

artist_router = APIRouter(prefix="/artist", tags=["Artist"])

@artist_router.get(
    "/{artist_id}",
    response_model=ArtistResponse,
    status_code=status.HTTP_200_OK
)
async def get_artist_by_id(
    artist_service: Annotated[ArtistService, Depends(get_artist_service)],
    artist_id: UUID
) -> Artist:
    return await artist_service.get_artist_by_id(artist_id)


@artist_router.get(
    "/{artist_mbid}",
    response_model=ArtistResponse,
    status_code=status.HTTP_200_OK
)
async def get_artist_by_mbid(
    artist_service: Annotated[ArtistService, Depends(get_artist_service)],
    artist_mbid: str
) -> Artist:
    return await artist_service.get_artist_by_mbid(artist_mbid)


@artist_router.get(
        "{artist_id}/albums",
        response_model=list[AlbumResponse],
        status_code=status.HTTP_200_OK
)
async def get_artist_albums(
    album_service: Annotated[AlbumService, Depends(get_album_service)],
    artist_id: UUID
) -> list[Album]:
    return await album_service.get_album_by_artist(artist_id)


@artist_router.get(
    "/",
    response_model=list[ArtistResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_artists(
    artist_service: Annotated[ArtistService, Depends(get_artist_service)],
    filters: Annotated[ArtistFiltersParams, Depends()]
) -> list[Artist]:
    return await artist_service.get_all_artist(filters.limit, filters.offset)