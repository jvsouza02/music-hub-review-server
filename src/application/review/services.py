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
from src.domain.track.exceptions import TrackNotFoundException
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
                raise TrackNotFoundException()

            artist_data = mbz_data["artist-credit"][0]["artist"]
            artist_mbid = artist_data["id"]

            artist = await self._artist_repository.get_by_mbid(artist_mbid)
            if artist is None:
                artist = Artist(
                    mbid=artist_mbid,
                    name=artist_data.get("name"),
                    disambiguation=artist_data.get("disambiguation"),
                    country=artist_data.get("country")
                )

                artist = await self._artist_repository.save(artist)

            release_data = mbz_data["releases"][0]
            album_mbid = release_data["id"]

            album = await self._album_repository.get_by_mbid(album_mbid)
            if album is None:
                album = Album(
                    mbid=album_mbid,
                    artist_id=artist.id,
                    title=release_data["title"],
                    release_date=release_data.get("date"),
                    total_tracks=release_data.get("track-count") or 0
                )

                album = await self._album_repository.save(album)

            media_list = release_data.get("media", [{}])
            first_media = media_list[0] if media_list else {}
            track_list = first_media.get("track-list", [{}])
            track_in_media = track_list[0] if track_list else {}
            track_position = track_in_media.get("position") or 1

            track = Track(
                mbid=mbz_data["id"],
                album_id=album.id,
                title=mbz_data.get("title"),
                position=track_position,
                duration_ms=mbz_data.get("length")
            )

            track = await self._track_repository.save(track)


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
