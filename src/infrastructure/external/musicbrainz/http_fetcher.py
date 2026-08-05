import logging

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter

from .token_bucket import TokenBucket

logger = logging.getLogger(__name__)


def _should_retry(exc: BaseException) -> bool:
    if isinstance(exc, (httpx.TimeoutException, httpx.ConnectError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {502, 503, 504}
    return False


class MusicBrainzFetcher:
    def __init__(
        self,
        base_url: str,
        headers: dict,
        timeout: float = 15.0,
        token_bucket: TokenBucket | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(headers=headers, timeout=timeout)
        self._bucket = token_bucket or TokenBucket(capacity=50.0, refill_rate=1.0)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    @retry(
        retry=retry_if_exception(_should_retry),
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        reraise=True,
    )
    async def fetch(self, endpoint: str, params: dict | None = None) -> dict | None:
        await self._bucket.acquire()

        query = {"fmt": "json", **(params or {})}
        url = f"{self.base_url}/{endpoint}"

        logger.info(f"MusicBrainz GET {url}")
        response = await self._client.get(url, params=query)

        if response.status_code == 404:
            return None

        if response.status_code >= 500:
            logger.warning(f"MusicBrainz {response.status_code} in {endpoint}")

        response.raise_for_status()
        return response.json()