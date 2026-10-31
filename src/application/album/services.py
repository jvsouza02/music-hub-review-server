from src.domain.album.entity import Album
from src.domain.album.repository import IAlbumRepository
from uuid import UUID


class AlbumService:
    def __init__(self, album_repository: IAlbumRepository):
        self._album_repository = album_repository

    async def get_album_by_id(self, album_id: UUID) -> Album:
        album = await self._album_repository.get_by_id(album_id)

        if album is None:
            raise Exception("Album not found.")

        return album


    async def get_album_by_mbid(self, album_mbid: str) -> Album:
        album = await self._album_repository.get_by_mbid(album_mbid)
        
        if album is None:
            raise Exception("Album not found.")
        
        return album


    async def get_albums_by_artist(self, artist_id: UUID) -> list[Album]:
        return await self._album_repository.get_by_artist(artist_id)


    async def get_all_albums(self, limit: int, offset: int) -> list[Album]:
        return await self._album_repository.get_all()
