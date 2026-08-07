from src.domain.artist.entity import Artist
from src.infrastructure.cache.redis_client import RedisClient

class ArtistCache:
    def __init__(self, redis: RedisClient, ttl_seconds: int = 3600):
        self._redis = redis
        self._ttl = ttl_seconds

    def _key(self, mbid: str) -> str:
        return f"Artist:{mbid}"

    async def get(self, mbid: str) -> Artist | None:
        raw = await self._redis.get(self._key(mbid))
        return Artist.model_validate_json(raw) if raw else None

    async def set(self, mbid: str, artist: Artist) -> None:
        return await self._redis.set(
            self._key(mbid),
            artist.model_dump_json(),
            self._ttl
        )

    async def delete(self, mbid: str) -> None:
        return await self._redis.delete(self._key(mbid))


    