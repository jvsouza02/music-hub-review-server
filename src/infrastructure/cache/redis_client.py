from typing import Any
from redis.asyncio import Redis
from src.core.config import settings


class RedisClient:
    def __init__(self, url: str = settings.REDIS_URL):
        self._client = Redis.from_url(url, decode_responses=True)

    async def get(self, key: str) -> str | None:
        return await self._client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        ttl: int = 3600,
    ) -> None:
        await self._client.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def eval(
        self,
        script: str,
        numkeys: int,
        *keys_and_args: str | int,
    ) -> Any:
        return await self._client.eval(
            script,
            numkeys,
            *keys_and_args,
        )

    async def close(self) -> None:
        await self._client.close()