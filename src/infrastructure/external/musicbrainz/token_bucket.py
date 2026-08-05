import asyncio
import logging
import time

logger = logging.getLogger(__name__)


class TokenBucket:
    def __init__(self, capacity: float = 50.0, refill_rate: float = 1.0):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill

            self.tokens = min(
                self.capacity,
                self.tokens + (elapsed * self.refill_rate),
            )
            self._last_refill = now

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                wait = 0.0
            else:
                wait = (1.0 - self.tokens) / self.refill_rate
                self.tokens -= 1.0

        if wait > 0:
            logger.debug(f"TokenBucket: awaiting {wait:.2f}s")
            await asyncio.sleep(wait)