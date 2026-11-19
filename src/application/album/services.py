from src.domain.album.entity import Album
from src.domain.album.repository import IAlbumRepository
from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from uuid import UUID


class AlbumService:
    def __init__(
        self,
        album_repository: IAlbumRepository,
        musicbrainz_client: IMusicBrainzClient             
    ):
        self._album_repository = album_repository
        self._musicbrainz_client = musicbrainz_client

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


    @staticmethod
    def _extract_artist_credit(
        artist_credit: list
    ) -> tuple[str | None, str | None]:
        artist_name_parts = []
        artist_mbid = None

        for credit in artist_credit:
            if not isinstance(credit, dict):
                continue

            artist = credit.get("artist") or {}

            name = credit.get("name") or artist.get("name")

            if name:
                artist_name_parts.append(
                    f"{name}{credit.get('joinphrase', '')}"
                )

            if not artist_mbid and artist.get("id"):
                artist_mbid = artist["id"]

        artist_name = "".join(artist_name_parts).strip() or None

        return artist_name, artist_mbid


    async def search_albums(self, query: str) -> list[dict]:
        normalized_query = query.strip()

        if not normalized_query:
            return []

        mbz_results = await self._musicbrainz_client.search(
            query=normalized_query,
            entity_type="release",
            limit=25
        )

        if not mbz_results:
            return []

        mbids = [
            item["id"]
            for item in mbz_results
            if item.get("id")
        ]

        if not mbids:
            return []

        local_albums = await self._album_repository.get_by_mbids(mbids)

        local_albums_map = {
            album.mbid.lower(): album
            for album in local_albums
        }

        results = []

        for item in mbz_results:
            mbid = item.get("id")
            title = item.get("title")

            if not mbid or not title:
                continue

            local_album = local_albums_map.get(mbid.lower())

            artist_name, artist_mbid = self._extract_artist_credit(
                item.get("artist-credit") or []
            )

            results.append({
                "mbid": mbid,
                "title": title,
                "artist_name": artist_name,
                "artist_mbid": artist_mbid,
                "release_date": item.get("date"),
                "total_tracks": item.get("track-count"),
                "average_score": (
                    float(local_album.average_score)
                    if local_album and local_album.average_score is not None
                    else None
                ),
                "review_count": (
                    local_album.review_count
                    if local_album
                    else 0
                ),
            })

        return results


    async def get_albums_by_artist(self, artist_id: UUID) -> list[Album]:
        return await self._album_repository.get_by_artist(artist_id)


    async def get_all_albums(self, limit: int, offset: int) -> list[Album]:
        return await self._album_repository.get_all(limit, offset)
