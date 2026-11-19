import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from fastapi import FastAPI

from src.main import lifespan
from src.presentation.api.v1.deps import get_musicbrainz_client


class MusicBrainzLifecycleTests(unittest.IsolatedAsyncioTestCase):

    @patch("src.main.MusicBrainzClient")
    async def test_client_is_created_and_closed(
        self,
        musicbrainz_client_factory,
    ):
        client = Mock()
        client.aclose = AsyncMock()

        musicbrainz_client_factory.return_value = client

        app = FastAPI()

        async with lifespan(app):
            self.assertIs(
                app.state.musicbrainz_client,
                client,
            )

            musicbrainz_client_factory.assert_called_once()
            client.aclose.assert_not_awaited()

        client.aclose.assert_awaited_once()

    def test_dependency_returns_application_client(self):
        expected_client = object()

        request = SimpleNamespace(
            app=SimpleNamespace(
                state=SimpleNamespace(
                    musicbrainz_client=expected_client,
                )
            )
        )

        result = get_musicbrainz_client(request)

        self.assertIs(result, expected_client)


if __name__ == "__main__":
    unittest.main()