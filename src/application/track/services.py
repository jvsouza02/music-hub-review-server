from src.domain.track.repository import ITrackRepository
from src.domain.track.entity import Track
from src.domain.track.exceptions import TrackNotFoundException
from uuid import UUID

class TrackService():
    def __init__(
            self,
            track_repository: ITrackRepository
    ):
        self.track_repository = track_repository


    async def get_track_by_id(self, track_id: UUID) -> Track:
        track = await self.track_repository.get_by_id(track_id)

        if track is None: 
            raise TrackNotFoundException()

        return track


    async def get_track_by_mbid(self, track_mbid: str) -> Track:
            track = await self.track_repository.get_by_mbid(track_mbid)
    
            if track is None: 
                raise TrackNotFoundException()
    
            return track


    async def get_track_by_album(self, album_id: UUID) -> list[Track]:
         return await self.track_repository.get_by_album(album_id)


    async def get_all_tracks(self, limit: int, offset: int) -> list[Track]:
         return await self.track_repository.get_all(limit, offset)

