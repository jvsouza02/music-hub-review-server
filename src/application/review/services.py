from uuid import UUID
from src.domain.review.entity import Review
from src.domain.review.repository import IReviewRepository
from src.domain.review.exceptions import ReviewAlreadyExistsException
from src.domain.artist.entity import Artist
from src.domain.artist.repository import IArtistRepository
from src.domain.album.entity import Album
from src.domain.album.repository import IAlbumRepository
from src.domain.track.entity import Track
from src.domain.track.repository import ITrackRepository
from src.domain.music.value_objects.score import Score
from src.application.interfaces.musicbrainz_client import IMusicBrainzClient

class ReviewService:
    def __init__(
            self,
            review_repository: IReviewRepository,
            artist_repository: IArtistRepository,
            album_repository: IAlbumRepository,
            track_repository: ITrackRepository,
            musicbrainz_client: IMusicBrainzClient
    ):
        self._review_repository = review_repository
        self._artist_repository = artist_repository
        self._album_repository = album_repository
        self._track_repository = track_repository
        self._musicbrainz_client = musicbrainz_client


    async def create_review(
            self,
            user_id: UUID,
            track_mbid: str,
            score_value: float,
            body: str | None,
    ) -> Review:
        score_obj = Score.from_float(score_value)

        track = await self._track_repository.get_by_mbid(track_mbid)
        if track is None:
            mbz_data = await self._musicbrainz_client.get_recording(track_mbid, inc="releases artists")

            if mbz_data is None:
                ...

            artist_data = mbz_data["artist-credit"][0]["artist"]
            artist_mbid = artist_data["id"]

            artist = await self._artist_repository.get_by_mbid(artist_mbid)
            if artist is None:
                ...


        review = await self._review_repository.get_by_user_and_track(user_id, track.id)
        if review:
            raise ReviewAlreadyExistsException()

        review = Review(
            user_id=user_id,
            track_id=track.id,
            score=score_obj,
            body=body
        )

        return await self._review_repository.save(review)
