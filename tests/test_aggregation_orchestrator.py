import unittest

from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

from src.application.aggregation.orchestrator import AggregationOrchestrator


class AggregationOrchestratorTests(unittest.IsolatedAsyncioTestCase):

    async def test_clears_album_and_artist_scores_when_no_tracks_are_reviewed(self):
        album_id = uuid4()
        artist_id = uuid4()

        album = SimpleNamespace(
            id=album_id,
            artist_id=artist_id,
            total_tracks=10,
            average_score=Decimal("4.5"),
            review_count=1,
        )

        artist = SimpleNamespace(
            id=artist_id,
            average_score=Decimal("4.5"),
            review_count=1,
        )

        track = SimpleNamespace(
            album_id=album_id,
        )

        unreviewed_track = SimpleNamespace(
            average_score=None,
            review_count=0,
        )

        track_repository = SimpleNamespace(
            get_by_album=AsyncMock(
                return_value=[unreviewed_track]
            )
        )

        async def update_album(album_id, data):
            album.average_score = data["average_score"]
            album.review_count = data["review_count"]

        album_repository = SimpleNamespace(
            get_by_id=AsyncMock(
                return_value=album
            ),
            get_by_artist=AsyncMock(
                return_value=[album]
            ),
            update=AsyncMock(
                side_effect=update_album
            ),
        )

        artist_repository = SimpleNamespace(
            get_by_id=AsyncMock(
                return_value=artist
            ),
            update=AsyncMock(),
        )

        await AggregationOrchestrator._cascade_album_and_artist(
            track,
            track_repository,
            album_repository,
            artist_repository,
        )

        album_repository.update.assert_awaited_once_with(
            album_id,
            {
                "average_score": None,
                "review_count": 0,
            },
        )

        artist_repository.update.assert_awaited_once_with(
            artist_id,
            {
                "average_score": None,
                "review_count": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()