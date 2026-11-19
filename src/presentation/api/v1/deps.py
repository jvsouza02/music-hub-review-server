from fastapi import Request

from src.application.interfaces.musicbrainz_client import IMusicBrainzClient


def get_musicbrainz_client(request: Request) -> IMusicBrainzClient:
    return request.app.state.musicbrainz_client