from fastapi import APIRouter, Depends, BackgroundTasks, status, Query
from typing import Annotated
from src.application.review.services import ReviewService
from src.application.aggregation.orchestrator import AggregationOrchestrator
from src.domain.user.entity import User
from src.domain.review.entity import Review
from .deps import get_review_service
from .schema import ReviewCreateRequest, ReviewResponse, ReviewUpdateRequest, ReviewFiltersParams
from ..auth.deps import get_current_user
from uuid import UUID

review_router = APIRouter(prefix="/review", tags=["Review"])

@review_router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_review(
    data: ReviewCreateRequest,
    background_task: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
) -> Review:
    review = await review_service.create_review(
        user_id=current_user.id,
        track_mbid=data.track_mbid,
        score_value=data.score,
        body=data.body
    )

    background_task.add_task(
        AggregationOrchestrator.run_aggregation_for_new_review,
        review.track_id,
        data.score 
    )

    return review


@review_router.get(
    "/{review_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReviewResponse
)
async def get_review_by_id(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    review_id: UUID,
) -> Review:
    return await review_service.get_review_by_id(review_id=review_id)


@review_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewResponse]
)
async def get_review_by_user(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    user_id: UUID,
    filters: Annotated[ReviewFiltersParams, Depends()]
) -> list[Review]:
    return await review_service.get_review_by_user(
        user_id=user_id,
        limit=filters.limit,
        offset=filters.offset,
    )

@review_router.get(
    "/{track_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewResponse]
)
async def get_review_by_track(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    track_id: UUID,
    filters: Annotated[ReviewFiltersParams, Depends()]
) -> list[Review]:
    return await review_service.get_review_by_track(
        track_id=track_id,
        limit=filters.limit,
        offset=filters.offset
    )


@review_router.put(
    "/{review_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK
)
async def update_review(
    review_id: UUID, 
    data: ReviewUpdateRequest,
    background_task: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    review_service: Annotated[ReviewService, Depends(get_review_service)]
) -> Review:
    updated_review, old_score_float = await review_service.update_review(
        review_id=review_id,
        current_user_id=current_user.id,
        new_score_value=data.new_score_value,
        new_body=data.new_body
    )

    if data.new_score_value is not None and old_score_float != data.new_score_value:
        background_task.add_task(
            AggregationOrchestrator.run_aggregation_for_updated_review,
            updated_review.track_id,
            old_score_float,
            data.new_score_value
        )

    return updated_review


@review_router.delete(
    "/{review_id}",
    status_code=status.HTTP_200_OK
)
async def delete_review(
    review_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    background_task: BackgroundTasks,
    review_service: Annotated[ReviewService, Depends(get_review_service)]
) -> Review:
    deleted_review, old_score_float = await review_service.delete_review(
        review_id=review_id,
        current_user_id=current_user.id
    )

    background_task.add_task(
        AggregationOrchestrator.run_aggregation_for_deleted_review,
        deleted_review.track_id,
        old_score_float
    )

    return deleted_review