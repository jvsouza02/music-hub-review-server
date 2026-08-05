import asyncio
import logging

from src.application.interfaces.musicbrainz_client import IMusicBrainzClient

from .constants import SEARCH_RESULT_KEYS
from .token_bucket import TokenBucket
from .circuit_breaker import CircuitBreaker, CircuitOpenError
from .cache import SimpleTTLCache
from .http_fetcher import MusicBrainzFetcher

logger = logging.getLogger(__name__)


class MusicBrainzClient(IMusicBrainzClient):
    def __init__(
        self,
        app_name: str,
        app_version: str,
        contact_email: str,
        base_url: str = "https://musicbrainz.org/ws/2",
        timeout: float = 15.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": f"{app_name}/{app_version} ( {contact_email} )",
            "Accept": "application/json",
        }

        self._bucket = TokenBucket(capacity=50.0, refill_rate=1.0)
        self._breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60.0)
        self._cache = SimpleTTLCache(max_size=10_000)
        self._fetcher = MusicBrainzFetcher(
            base_url=base_url,
            headers=self.headers,
            timeout=timeout,
            token_bucket=self._bucket,
        )

        self._inflight: dict[str, asyncio.Future] = {}
        self._inflight_lock = asyncio.Lock()

        self._TTL_LOOKUP = 7 * 24 * 3600 
        self._TTL_SEARCH = 3600         
        self._TTL_BROWSE = 3600            

    async def aclose(self) -> None:
        await self._fetcher.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    def _cache_key(self, endpoint: str, params: dict | None) -> str:
        params_str = str(sorted(params.items())) if params else ""
        return f"{endpoint}:{params_str}"

    async def _get(self, endpoint: str, params: dict | None, ttl: int):
        cache_key = self._cache_key(endpoint, params)
        cached = self._cache.get(cache_key, ttl)
        if cached is not ...:
            return cached

        async with self._inflight_lock:
            if cache_key in self._inflight:
                future = self._inflight[cache_key]
                return await future

            future = asyncio.get_event_loop().create_future()
            self._inflight[cache_key] = future

        try:
            data = await self._breaker.call(self._fetcher.fetch, endpoint, params)
            self._cache.set(cache_key, data, ttl)
            future.set_result(data)
            return data

        except Exception as exc:
            future.set_exception(exc)
            raise
        finally:
            async with self._inflight_lock:
                self._inflight.pop(cache_key, None)


    async def search(self, query: str, entity_type: str, limit: int = 25, offset: int = 0) -> list[dict]:
        key = SEARCH_RESULT_KEYS.get(entity_type)
        if not key:
            raise ValueError(f"Tipo não suportado: {entity_type}")
        data = await self._get(entity_type, {"query": query, "limit": limit, "offset": offset}, self._TTL_SEARCH)
        return data.get(key, []) if data else []

    async def get_artist(self, mbid: str, inc: str | None = None) -> dict | None:
        return await self._get(f"artist/{mbid}", {"inc": inc} if inc else None, self._TTL_LOOKUP)

    async def get_release_group(self, mbid: str, inc: str | None = None) -> dict | None:
        return await self._get(f"release-group/{mbid}", {"inc": inc} if inc else None, self._TTL_LOOKUP)

    async def get_album(self, mbid: str, inc: str | None = None) -> dict | None:
        return await self.get_release_group(mbid, inc)

    async def get_release(self, mbid: str, inc: str | None = None) -> dict | None:
        return await self._get(f"release/{mbid}", {"inc": inc} if inc else None, self._TTL_LOOKUP)

    async def get_recording(self, mbid: str, inc: str | None = None) -> dict | None:
        return await self._get(f"recording/{mbid}", {"inc": inc} if inc else None, self._TTL_LOOKUP)

    async def browse_recordings_by_artist(self, artist_mbid: str, limit: int = 25, offset: int = 0) -> list[dict]:
        data = await self._get("recording", {"artist": artist_mbid, "limit": limit, "offset": offset}, self._TTL_BROWSE)
        return data.get("recordings", []) if data else []