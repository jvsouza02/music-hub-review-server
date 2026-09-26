from src.infrastructure.database.album.model import AlbumModel
from src.domain.album.entity import Album

class AlbumMapper:
    @staticmethod
    def to_entity(model: AlbumModel) -> Album:
        return Album.model_validate(model)

    @staticmethod
    def to_model(entity: Album) -> AlbumModel:
        return AlbumModel(**entity.model_dump())