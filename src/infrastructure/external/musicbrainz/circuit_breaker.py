import asyncio
import logging
import time

logger = logging.getLogger(__name__)


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failures = 0
        self._last_failure = 0.0
        self._state = "closed"
        self._lock = asyncio.Lock()

    async def call(self, coro, *args, **kwargs):
        async with self._lock:
            if self._state == "open":
                if time.monotonic() - self._last_failure >= self.recovery_timeout:
                    self._state = "half_open"
                    logger.info("CircuitBreaker: HALF_OPEN")
                else:
                    raise CircuitOpenError("Circuit Breaker OPEN")
                
        try:
            result = await coro(*args, **kwargs)

            async with self._lock:
                if self._state == "half_open":
                    self._state = "closed"
                    logger.info("CircuitBreaker: CLOSED")
                self._failures = 0
            return result

        except Exception:
            async with self._lock:
                self._failures += 1
                self._last_failure = time.monotonic()
                if self._failures >= self.failure_threshold:
                    self._state = "open"
                    logger.error(f"CircuitBreaker: OPEN ({self._failures} falhas)")
            raise