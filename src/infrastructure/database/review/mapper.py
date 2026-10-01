from src.domain.review.entity import Review
from src.infrastructure.database.review.model import ReviewModel
from src.domain.music.value_objects.score import Score

class ReviewMapper:
    @staticmethod
    def to_entity(model: ReviewModel) -> Review:
        score_obj = Score.from_float(float(model.score))

        return Review(
            id=model.id,
            user_id=model.user_id,
            track_id=model.track_id,
            score=score_obj,
            body=model.body,
            is_active=model.is_active,
            is_edited=model.is_edited,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Review) -> ReviewModel:
        data = entity.model_dump()

        if hasattr(entity.score, "value"):
            data["score"] = entity.score.value
        elif isinstance(data.get("score"), dict):
            data["score"] = data["score"].get("value")

        return ReviewModel(**data)