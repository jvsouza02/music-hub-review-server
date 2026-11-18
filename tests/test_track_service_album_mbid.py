import unittest
from uuid import uuid4

from src.application.track.services import TrackService
from src.domain.track.entity import Track


class FakeTrackRepository:
    def __init__(self):
        self.track_by_id = None
        self.tracks_by_mbid = {}
        self.all_tracks = []

    async def get_by_id_with_album_mbid(self, track_id):
        if self.track_by_id is None:
            return None

        track, album_mbid = self.track_by_id

        if track.id != track_id:
            return None

        return track, album_mbid

    async def get_by_mbids_with_album_mbids(self, mbids):
        return [
            self.tracks_by_mbid[mbid]
            for mbid in mbids
            if mbid in self.tracks_by_mbid
        ]

    async def get_all_with_album_mbids(self, limit, offset):
        return self.all_tracks[offset:offset + limit]


class FakeMusicBrainzClient:
    def __init__(self):
        self.search_results = []
        self.recordings = {}

    async def search(self, **kwargs):
        return self.search_results

    async def get_recording(self, mbid, inc=None):
        return self.recordings.get(mbid)


def make_track():
    return Track(
        mbid=str(uuid4()),
        album_id=uuid4(),
        title="Test Track",
        position=1,
        duration_ms=180000,
    )


class TrackServiceAlbumMbidTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.repository = FakeTrackRepository()
        self.musicbrainz = FakeMusicBrainzClient()

        self.service = TrackService(
            self.repository,
            self.musicbrainz,
        )

    async def test_get_track_by_id_includes_album_mbid(self):
        track = make_track()
        album_mbid = uuid4()

        self.repository.track_by_id = (track, str(album_mbid))

        result = await self.service.get_track_by_id(track.id)

        self.assertEqual(result["album_mbid"], str(album_mbid))
        self.assertEqual(result["mbid"], track.mbid)

    async def test_get_all_tracks_includes_album_mbid(self):
        track = make_track()
        album_mbid = str(uuid4())

        self.repository.all_tracks = [
            (track, album_mbid)
        ]

        result = await self.service.get_all_tracks(
            limit=20,
            offset=0,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["album_mbid"], album_mbid)

    async def test_search_prefers_album_associated_in_database(self):
        track = make_track()

        local_album_mbid = str(uuid4())
        musicbrainz_album_mbid = str(uuid4())

        self.repository.tracks_by_mbid[track.mbid] = (
            track,
            local_album_mbid,
        )

        self.musicbrainz.search_results = [
            {
                "id": track.mbid,
                "title": "Test Track",
                "artist-credit": [
                    {"name": "Test Artist"}
                ],
                "releases": [
                    {
                        "id": musicbrainz_album_mbid,
                        "title": "MusicBrainz Album",
                    }
                ],
            }
        ]

        result = await self.service.search_tracks("Test Track")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["album_mbid"], local_album_mbid)

    async def test_search_uses_musicbrainz_album_when_track_is_not_local(self):
        track_mbid = str(uuid4())
        album_mbid = str(uuid4())

        self.musicbrainz.search_results = [
            {
                "id": track_mbid,
                "title": "External Track",
                "artist-credit": [
                    {"name": "External Artist"}
                ],
                "releases": [
                    {
                        "id": album_mbid,
                        "title": "External Album",
                    }
                ],
            }
        ]

        result = await self.service.search_tracks("External Track")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["album_mbid"], album_mbid)

    async def test_track_details_prefers_local_album(self):
        track = make_track()

        local_album_mbid = str(uuid4())
        musicbrainz_album_mbid = str(uuid4())

        self.repository.tracks_by_mbid[track.mbid] = (
            track,
            local_album_mbid,
        )

        self.musicbrainz.recordings[track.mbid] = {
            "id": track.mbid,
            "title": track.title,
            "artist-credit": [],
            "releases": [
                {
                    "id": musicbrainz_album_mbid,
                    "title": "MusicBrainz Album",
                }
            ],
        }

        result = await self.service.get_track_by_mbid(track.mbid)

        self.assertEqual(result["album_mbid"], local_album_mbid)