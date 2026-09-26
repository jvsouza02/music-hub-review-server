from src.domain.track.entity import Track
from src.infrastructure.database.track.model import TrackModel

class TrackMapper:
    @staticmethod
    def to_entity(model: TrackModel) -> Track:
        return Track.model_validate(model)

    @staticmethod
    def to_model(entity: Track) -> TrackModel:
        return TrackModel(**entity.model_dump())