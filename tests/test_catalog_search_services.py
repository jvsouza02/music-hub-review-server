import unittest

from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from src.application.artist.services import ArtistService
from src.application.album.services import AlbumService


class FakeMusicBrainzClient:
    def __init__(self):
        self.results = {
            "artist": [],
            "release": [],
        }
        self.calls = []

    async def search(
        self,
        query: str,
        entity_type: str,
        limit: int = 25,
        offset: int = 0,
    ):
        self.calls.append({
            "query": query,
            "entity_type": entity_type,
            "limit": limit,
            "offset": offset,
        })

        return self.results.get(entity_type, [])


class FakeArtistRepository:
    def __init__(self):
        self.artists = []
        self.received_mbids = []

    async def get_by_mbids(self, artist_mbids):
        self.received_mbids = artist_mbids

        mbids = set(artist_mbids)

        return [
            artist
            for artist in self.artists
            if artist.mbid in mbids
        ]


class FakeAlbumRepository:
    def __init__(self):
        self.albums = []
        self.received_mbids = []

    async def get_by_mbids(self, album_mbids):
        self.received_mbids = album_mbids

        mbids = set(album_mbids)

        return [
            album
            for album in self.albums
            if album.mbid in mbids
        ]


class CatalogSearchServiceTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.musicbrainz = FakeMusicBrainzClient()

        self.artist_repository = FakeArtistRepository()
        self.album_repository = FakeAlbumRepository()

        self.artist_service = ArtistService(
            self.artist_repository,
            self.musicbrainz,
        )

        self.album_service = AlbumService(
            self.album_repository,
            self.musicbrainz,
        )

    async def test_artist_search_merges_local_ratings(self):
        artist_mbid = str(uuid4())

        self.musicbrainz.results["artist"] = [
            {
                "id": artist_mbid,
                "name": "Radiohead",
                "disambiguation": "English alternative rock band",
                "country": "GB",
            }
        ]

        self.artist_repository.artists = [
            SimpleNamespace(
                mbid=artist_mbid,
                average_score=Decimal("4.8"),
                review_count=12,
            )
        ]

        results = await self.artist_service.search_artists(" Radiohead ")

        self.assertEqual(len(results), 1)

        self.assertEqual(results[0]["mbid"], artist_mbid)
        self.assertEqual(results[0]["name"], "Radiohead")
        self.assertEqual(results[0]["average_score"], 4.8)
        self.assertEqual(results[0]["review_count"], 12)

        self.assertEqual(
            self.musicbrainz.calls[0]["entity_type"],
            "artist",
        )

        self.assertEqual(
            self.musicbrainz.calls[0]["query"],
            "Radiohead",
        )

    async def test_artist_without_local_record_has_no_rating(self):
        artist_mbid = str(uuid4())

        self.musicbrainz.results["artist"] = [
            {
                "id": artist_mbid,
                "name": "External Artist",
            }
        ]

        results = await self.artist_service.search_artists(
            "External Artist"
        )

        self.assertEqual(len(results), 1)
        self.assertIsNone(results[0]["average_score"])
        self.assertEqual(results[0]["review_count"], 0)

    async def test_album_search_merges_local_ratings_and_artist_credit(self):
        album_mbid = str(uuid4())
        artist_mbid = str(uuid4())

        self.musicbrainz.results["release"] = [
            {
                "id": album_mbid,
                "title": "Meteora",
                "date": "2003-03-25",
                "track-count": 13,
                "artist-credit": [
                    {
                        "name": "Linkin Park",
                        "artist": {
                            "id": artist_mbid,
                            "name": "Linkin Park",
                        },
                    }
                ],
            }
        ]

        self.album_repository.albums = [
            SimpleNamespace(
                mbid=album_mbid,
                average_score=Decimal("4.7"),
                review_count=20,
            )
        ]

        results = await self.album_service.search_albums("Meteora")

        self.assertEqual(len(results), 1)

        self.assertEqual(results[0]["mbid"], album_mbid)
        self.assertEqual(results[0]["title"], "Meteora")
        self.assertEqual(results[0]["artist_name"], "Linkin Park")
        self.assertEqual(results[0]["artist_mbid"], artist_mbid)
        self.assertEqual(results[0]["total_tracks"], 13)

        self.assertEqual(results[0]["average_score"], 4.7)
        self.assertEqual(results[0]["review_count"], 20)

        self.assertEqual(
            self.musicbrainz.calls[0]["entity_type"],
            "release",
        )

    async def test_album_without_local_record_has_no_rating(self):
        album_mbid = str(uuid4())

        self.musicbrainz.results["release"] = [
            {
                "id": album_mbid,
                "title": "External Album",
            }
        ]

        results = await self.album_service.search_albums(
            "External Album"
        )

        self.assertEqual(len(results), 1)
        self.assertIsNone(results[0]["average_score"])
        self.assertEqual(results[0]["review_count"], 0)
        self.assertIsNone(results[0]["artist_mbid"])

    async def test_blank_queries_do_not_call_musicbrainz(self):
        artist_results = await self.artist_service.search_artists("   ")
        album_results = await self.album_service.search_albums("   ")

        self.assertEqual(artist_results, [])
        self.assertEqual(album_results, [])
        self.assertEqual(self.musicbrainz.calls, [])


if __name__ == "__main__":
    unittest.main()