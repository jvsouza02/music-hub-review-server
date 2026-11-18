from src.domain.track.repository import ITrackRepository
from src.domain.track.entity import Track
from src.domain.track.exceptions import TrackNotFoundException
from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from uuid import UUID
from typing import Any

class TrackService():
    def __init__(
            self,
            track_repository: ITrackRepository,
            musicbrainz_client: IMusicBrainzClient
    ):
        self._track_repository = track_repository
        self._musicbrainz_client = musicbrainz_client


    async def get_track_by_id(self, track_id: UUID) -> dict[str, Any]:
        result = await self._track_repository.get_by_id_with_album_mbid(
            track_id
        )

        if result is None:
            raise TrackNotFoundException()

        track, album_mbid = result

        return {
            **track.model_dump(),
            "album_mbid": album_mbid,
        }


    async def get_track_by_mbid(self, track_mbid: str) -> dict:
        mbz_data = await self._musicbrainz_client.get_recording(
            track_mbid,
            inc="releases artists"
        )

        if mbz_data is None:
            raise TrackNotFoundException()

        local_tracks = (
            await self._track_repository.get_by_mbids_with_album_mbids(
                [track_mbid]
            )
        )

        if local_tracks:
            local_track, local_album_mbid = local_tracks[0]
        else:
            local_track = None
            local_album_mbid = None

        artist_name = self._extract_artist_name(
            mbz_data.get("artist-credit") or []
        )

        releases = mbz_data.get("releases") or []
        release = releases[0] if releases else {}

        album_title = release.get("title")

        position = None

        for release_item in releases:
            for medium in release_item.get("media") or []:
                tracks = medium.get("tracks") or medium.get("track-list") or []

                for release_track in tracks:
                    recording = release_track.get("recording") or {}

                    if recording.get("id") == track_mbid:
                        raw_position = (
                            release_track.get("position")
                            or release_track.get("number")
                        )

                        try:
                            position = int(raw_position)
                        except (TypeError, ValueError):
                            position = None

                        break

                if position is not None:
                    break

            if position is not None:
                break

        return {
            "id": local_track.id if local_track else None,
            "mbid": mbz_data["id"],
            "album_id": local_track.album_id if local_track else None,
            "album_mbid": local_album_mbid or release.get("id"),
            "title": mbz_data["title"],
            "artist_name": artist_name,
            "album_title": album_title,
            "position": position,
            "duration_ms": mbz_data.get("length"),
            "average_score": (
                float(local_track.average_score)
                if local_track and local_track.average_score is not None
                else None
            ),
            "review_count": local_track.review_count if local_track else 0,
        }


    async def search_tracks(self, query: str) -> list[dict]:
        smart_query = self._build_smart_query(query)

        mbz_results = await self._musicbrainz_client.search(
            query=smart_query,
            entity_type="recording",
            limit=25
        )

        if not mbz_results:
            return []

        mbids = [item["id"] for item in mbz_results]

        local_tracks = (
            await self._track_repository.get_by_mbids_with_album_mbids(
                mbids
            )
        )

        local_tracks_map = {
            track.mbid: (track, album_mbid)
            for track, album_mbid in local_tracks
        }

        results = []

        for item in mbz_results:
            mbid = item["id"]

            artist_credit = item.get("artist-credit", [{}])
            artist_name = (
                artist_credit[0].get("name")
                if artist_credit
                else "Unknown Artist"
            )

            releases = item.get("releases") or []
            release = releases[0] if releases else {}

            album_name = (
                release.get("title")
                if releases
                else "Single/Unknown"
            )

            local_track_data = local_tracks_map.get(mbid)

            if local_track_data:
                local_track, local_album_mbid = local_track_data
            else:
                local_track = None
                local_album_mbid = None

            results.append({
                "mbid": mbid,
                "title": item.get("title"),
                "artist_name": artist_name,
                "album_title": album_name,
                "album_mbid": local_album_mbid or release.get("id"),
                "average_score": (
                    local_track.average_score
                    if local_track
                    else None
                ),
                "review_count": (
                    local_track.review_count
                    if local_track
                    else 0
                ),
            })

        return results


    async def get_track_by_album(self, album_id: UUID) -> list[Track]:
         return await self._track_repository.get_by_album(album_id)


    async def get_all_tracks(
        self,
        limit: int,
        offset: int
    ) -> list[dict[str, Any]]:
        tracks = await self._track_repository.get_all_with_album_mbids(
            limit,
            offset
        )

        return [
            {
                **track.model_dump(),
                "album_mbid": album_mbid,
            }
            for track, album_mbid in tracks
        ]


    def _build_smart_query(self, user_query: str) -> str:
        clean_query = "".join(c for c in user_query if c.isalnum() or c.isspace()).strip()
        terms = clean_query.split()
        
        if not terms:
            return ""

        conditions = []
        for term in terms:
            conditions.append(f"(recording:{term} OR artist:{term} OR release:{term})")
        
        flexible_query = " AND ".join(conditions)

        exact_boost = f'recording:"{clean_query}"^2'

        return f"({exact_boost}) OR ({flexible_query})"


    @staticmethod
    def _extract_artist_name(artist_credit: list) -> str:
        parts = []

        for credit in artist_credit:
            if not isinstance(credit, dict):
                continue

            name = credit.get("name")

            if not name:
                artist = credit.get("artist") or {}
                name = artist.get("name", "")

            parts.append(f"{name}{credit.get('joinphrase', '')}")

        return "".join(parts).strip() or "Unknown Artist"

