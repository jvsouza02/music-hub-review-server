from fastapi import APIRouter, Depends, BackgroundTasks, status
from typing import Annotated
from src.application.review.services import ReviewService
from src.domain.user.entity import User
from src.domain.review.entity import Review
from .deps import get_review_service
from .schema import ReviewCreateRequest, ReviewResponse
from ..auth.deps import get_current_user
from uuid import UUID

review_router = APIRouter(prefix="/review", tags=["Review"])

async def mock_recalculate_score(track_id: UUID):
    print(f"Recalculanto notas para: {track_id}")

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

    background_task.add_task(mock_recalculate_score, review.track_id)

    return review