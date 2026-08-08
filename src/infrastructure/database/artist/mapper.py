from src.domain.artist.entity import Artist
from src.infrastructure.database.artist.model import ArtistModel

class ArtistMapper:
    @staticmethod
    def to_entity(model: ArtistModel) -> Artist:
        return Artist.model_validate(model)

    @staticmethod
    def to_model(entity: Artist) -> ArtistModel:
        return ArtistModel(**entity.model_dump())