import time
import logging

logger = logging.getLogger(__name__)


class SimpleTTLCache:
    def __init__(self, max_size: int = 10_000):
        self._data: dict[str, tuple[float, object]] = {}
        self._max_size = max_size

    def get(self, key: str, ttl: int) -> object:

        if key not in self._data:
            return ...

        expires_at, value = self._data[key]
        if time.monotonic() > expires_at:
            del self._data[key]
            return ...

        logger.debug(f"Cache HIT: {key}")
        return value

    def set(self, key: str, value: object, ttl: int) -> None:
        if len(self._data) >= self._max_size:
            oldest_keys = sorted(self._data, key=lambda k: self._data[k][0])[: self._max_size // 10]
            for k in oldest_keys:
                del self._data[k]

        self._data[key] = (time.monotonic() + ttl, value)