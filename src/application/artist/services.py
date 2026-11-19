from src.domain.artist.entity import Artist
from src.domain.artist.exceptions import ArtistNotFoundException
from src.domain.artist.repository import IArtistRepository
from src.application.interfaces.musicbrainz_client import IMusicBrainzClient
from uuid import UUID

class ArtistService:
    def __init__(
        self,
        artist_repository: IArtistRepository,
        musicbrainz_client: IMusicBrainzClient
    ):
        self._artist_repository = artist_repository
        self._musicbrainz_client = musicbrainz_client


    async def get_artist_by_id(self, artist_id: UUID) -> Artist:
        artist = await self._artist_repository.get_by_id(artist_id)

        if artist is None:
            raise ArtistNotFoundException()

        return artist


    async def get_artist_by_mbid(self, artist_mbid: str) -> Artist:
        artist = await self._artist_repository.get_by_mbid(artist_mbid)

        if artist is None:
            raise ArtistNotFoundException()

        return artist


    async def search_artists(self, query: str) -> list[dict]:
        normalized_query = query.strip()

        if not normalized_query:
            return []

        mbz_results = await self._musicbrainz_client.search(
            query=normalized_query,
            entity_type="artist",
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

        local_artists = await self._artist_repository.get_by_mbids(mbids)

        local_artists_map = {
            artist.mbid.lower(): artist
            for artist in local_artists
        }

        results = []

        for item in mbz_results:
            mbid = item.get("id")
            name = item.get("name")

            if not mbid or not name:
                continue

            local_artist = local_artists_map.get(mbid.lower())

            results.append({
                "mbid": mbid,
                "name": name,
                "disambiguation": item.get("disambiguation"),
                "country": item.get("country"),
                "average_score": (
                    float(local_artist.average_score)
                    if local_artist and local_artist.average_score is not None
                    else None
                ),
                "review_count": (
                    local_artist.review_count
                    if local_artist
                    else 0
                ),
            })

        return results


    async def get_all_artist(self, limit: int, offset = 0) -> list[Artist]:
        return await self._artist_repository.get_all(limit, offset)

