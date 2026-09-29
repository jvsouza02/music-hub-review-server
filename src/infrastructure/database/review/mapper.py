from src.domain.review.entity import Review
from src.infrastructure.database.review.model import ReviewModel

class ReviewMapper:
    @staticmethod
    def to_entity(model: ReviewModel) -> Review:
        return Review.model_validate(model)

    @staticmethod
    def to_model(entity: Review) -> ReviewModel:
        return ReviewModel(**entity.model_dump())