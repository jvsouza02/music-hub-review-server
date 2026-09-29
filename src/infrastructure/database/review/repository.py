from src.domain.review.repository import IReviewRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from src.domain.review.entity import Review
from src.infrastructure.database.review.mapper import ReviewMapper
from src.infrastructure.database.review.model import ReviewModel
from uuid import UUID
from sqlalchemy import select, update
from typing import Any

class ReviewRepository(IReviewRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, review: Review) -> Review:
        review_model = ReviewMapper.to_model(review)

        try:
            self._session.add(review_model)
            await self._session.commit()
        except DBAPIError as error:
            await self._session.rollback()
            raise error

        return ReviewMapper.to_entity(review_model)


    async def get_by_id(self, review_id: UUID) -> Review | None:
        statement = select(ReviewModel).where(
            ReviewModel.review_id == review_id,
            Review.is_active == True
        )

        result = await self._session.execute(statement)
        review_model = result.scalar_one_or_none()

        if review_model is None:
            return None

        return ReviewMapper.to_entity(review_model)


    async def get_by_user(self, user_id: UUID) -> list[Review]:
        statement = select(ReviewModel).where(
            ReviewModel.user_id == user_id,
            Review.is_active == True
        )
        result = await self._session.execute(statement)

        return [ReviewMapper.to_entity(review) for review in result.scalars().all()]


    async def get_by_track(self, track_id: UUID) -> list[Review]:
        statement = select(ReviewModel).where(
            ReviewModel.track_id == track_id,
            Review.is_active == True
        )
        result = await self._session.execute(statement)

        return [ReviewMapper.to_entity(review) for review in result.scalars().all()]


    async def get_by_user_and_track(self, user_id: UUID, track_id: UUID) -> Review | None:
        statement = select(ReviewModel).where(
            ReviewModel.user_id == user_id,
            ReviewModel.track_id == track_id,
            ReviewModel.is_active == True
        )

        result = await self._session.execute(statement)
        review_model = result.scalar_one_or_none()

        if review_model is None:
            return None

        return ReviewMapper.to_entity(review_model)


    async def update(self, review_id: UUID, update_data: dict[str, Any]) -> Review | None:
        if not update_data:
            return None

        statement = (
            update(ReviewModel)
            .where(ReviewModel.review_id == review_id)
            .values(**update_data)
            .returning(ReviewModel)
        )

        result = await self._session.execute(statement)
        await self._session.commit()

        updated_model = result.scalar_one_or_none()

        if updated_model is None:
            return None

        return ReviewMapper.to_entity(updated_model)


    async def delete(self, review_id: UUID) -> bool:
        statement = (
            update(ReviewModel)
            .where(ReviewModel.review_id == review_id)
            .values(is_active=False)
        )

        result = await self._session.execute(statement)
        await self._session.commit()

        return result.rowcount > 0
        