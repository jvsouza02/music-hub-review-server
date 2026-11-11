from fastapi import APIRouter, Depends, status, Query
from .schema import TrackResponse, TrackFiltersParams, TrackSearchResult
from .deps import get_track_service
from src.domain.track.entity import Track
from src.application.track.services import TrackService
from typing import Annotated
from uuid import UUID

track_router = APIRouter(prefix="/tracks", tags=["Track"])


@track_router.get(
        "/search",
        response_model=list[TrackSearchResult],
        status_code=status.HTTP_200_OK,
        operation_id="searchTracks"
)
async def search_track(
    track_service: Annotated[TrackService, Depends(get_track_service)],
    query: Annotated[str, Query()]
) -> list[dict]:
    return await track_service.search_tracks(query)

@track_router.get(
    "/id/{track_id}",
    response_model=TrackResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getTrackById"
)
async def get_track_by_id(
    track_service: Annotated[TrackService, Depends(get_track_service)],
    track_id: UUID
) -> Track:
    return await track_service.get_track_by_id(track_id)


@track_router.get(
    "/mbid/{track_mbid}",
    response_model=TrackResponse,
    status_code=status.HTTP_200_OK,
    operation_id="getTrackByMbid"
)
async def get_track_by_mbid(
    track_service: Annotated[TrackService, Depends(get_track_service)],
    track_mbid: UUID
) -> Track:
    return await track_service.get_track_by_id(track_mbid)


@track_router.get(
    "/",
    response_model=list[TrackResponse],
    status_code=status.HTTP_200_OK,
    operation_id="listTracks"
)
async def get_all_tracks(
    track_service: Annotated[TrackService, Depends(get_track_service)],
    filters: Annotated[TrackFiltersParams, Query()]
) -> list[Track]:
    return await track_service.get_all_tracks(filters.limit, filters.offset)