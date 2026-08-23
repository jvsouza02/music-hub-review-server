from abc import ABC, abstractmethod
from src.domain.review.entity import Review
from uuid import UUID
from typing import Any

class IReviewRepository(ABC):
    @abstractmethod
    async def save(self, review: Review) -> Review:
        ...

    @abstractmethod
    async def get_by_id(self, review_id: UUID) -> Review | None:
        ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[Review]:
        ...

    @abstractmethod
    async def get_by_track(self, track_id: UUID) -> list[Review]:
        ...

    @abstractmethod
    async def get_by_user_and_track(
        self,
        user_id: UUID,
        track_id: UUID
    ) -> Review | None:
        ...

    @abstractmethod
    async def update(
        self,
        review_id: UUID,
        update_data: dict[str, Any]
    ) -> Review | None:
        ...

    @abstractmethod
    async def delete(self, review_id: UUID) -> bool:
        ...