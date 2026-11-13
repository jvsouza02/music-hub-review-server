import logging
from uuid import uuid4

from src.core.config import settings
from src.infrastructure.cache.redis_client import RedisClient

logger = logging.getLogger(__name__)


_CREATE_SCRIPT = """
if redis.call("EXISTS", KEYS[1]) == 1
    or redis.call("EXISTS", KEYS[2]) == 1 then
    return 0
end

redis.call("SET", KEYS[1], ARGV[1], "EX", ARGV[3])
redis.call("SET", KEYS[2], ARGV[2], "EX", ARGV[3])

return 1
"""


_ROTATE_SCRIPT = """
local expected_family_id = ARGV[1]
local presented_jti = ARGV[2]
local new_jti = ARGV[3]
local used_ttl = tonumber(ARGV[4])
local active_ttl = tonumber(ARGV[5])

-- Um token encontrado no histórico já foi utilizado.
-- Sua reutilização revoga a família.
local used_family_id = redis.call("GET", KEYS[3])

if used_family_id then
    if used_family_id == expected_family_id then
        local current_jti = redis.call("GET", KEYS[2])

        if current_jti then
            redis.call("DEL", "refresh:" .. current_jti)
        end

        redis.call("DEL", KEYS[2])

        return -1
    end

    return 0
end

-- Verifica se o token apresentado pertence à família.
local stored_family_id = redis.call("GET", KEYS[1])

if not stored_family_id then
    return 0
end

if stored_family_id ~= expected_family_id then
    return 0
end

-- Recupera o token atualmente ativo na família.
local current_jti = redis.call("GET", KEYS[2])

if not current_jti then
    redis.call("DEL", KEYS[1])
    return 0
end

-- O token ainda possui registro ativo, mas não é o atual.
-- Trata-se de reutilização ou inconsistência.
if current_jti ~= presented_jti then
    redis.call("DEL", "refresh:" .. current_jti)
    redis.call("DEL", KEYS[2])

    return -1
end

-- Rotação legítima.
redis.call("DEL", KEYS[1])

-- Preserva o identificador consumido até sua expiração original.
redis.call(
    "SET",
    KEYS[3],
    stored_family_id,
    "EX",
    used_ttl
)

-- Cria o novo refresh token.
redis.call(
    "SET",
    "refresh:" .. new_jti,
    stored_family_id,
    "EX",
    active_ttl
)

-- Atualiza a referência da família.
redis.call(
    "SET",
    KEYS[2],
    new_jti,
    "EX",
    active_ttl
)

return 1
"""


_REVOKE_FAMILY_SCRIPT = """
local current_jti = redis.call("GET", KEYS[1])

if current_jti then
    redis.call("DEL", "refresh:" .. current_jti)
end

redis.call("DEL", KEYS[1])

return 1
"""


_REVOKE_BY_JTI_SCRIPT = """
local family_id = redis.call("GET", KEYS[1])

if not family_id then
    family_id = redis.call("GET", KEYS[2])
end

if not family_id then
    return 0
end

local current_jti = redis.call(
    "GET",
    "refresh_family:" .. family_id
)

if current_jti then
    redis.call("DEL", "refresh:" .. current_jti)
end

redis.call("DEL", "refresh_family:" .. family_id)

return 1
"""


class RefreshTokenStore:
    """
    Gerencia refresh tokens no Redis com rotação e detecção
    de reutilização.

    Cada família possui somente um refresh token ativo.
    Os identificadores consumidos são preservados até sua
    expiração original.
    """

    def __init__(self, redis: RedisClient):
        self._redis = redis
        self._ttl_seconds = (
            settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

    def _key(self, jti: str) -> str:
        return f"refresh:{jti}"

    def _family_key(self, family_id: str) -> str:
        return f"refresh_family:{family_id}"

    def _used_key(self, jti: str) -> str:
        return f"refresh_used:{jti}"

    async def create(self, user_id: str) -> tuple[str, str]:
        """
        Cria uma nova família e seu primeiro refresh token.

        Retorna (jti, family_id).
        """

        for _ in range(3):
            jti = str(uuid4())
            family_id = str(uuid4())

            created = await self._redis.eval(
                _CREATE_SCRIPT,
                2,
                self._key(jti),
                self._family_key(family_id),
                family_id,
                jti,
                self._ttl_seconds,
            )

            if int(created) == 1:
                logger.debug("Refresh token family created.")
                return jti, family_id

        raise RuntimeError(
            "Could not create a unique refresh token family."
        )

    async def validate_and_rotate(
        self,
        jti: str,
        expected_family_id: str,
        used_ttl: int,
    ) -> tuple[str, str] | None:
        """
        Valida e rotaciona um refresh token atomicamente.

        Retorna (novo_jti, family_id) se válido.
        Retorna None se inválido ou reutilizado.
        """

        new_jti = str(uuid4())

        result = await self._redis.eval(
            _ROTATE_SCRIPT,
            3,
            self._key(jti),
            self._family_key(expected_family_id),
            self._used_key(jti),
            expected_family_id,
            jti,
            new_jti,
            max(1, used_ttl),
            self._ttl_seconds,
        )

        status = int(result)

        if status == 1:
            logger.debug("Refresh token successfully rotated.")
            return new_jti, expected_family_id

        if status == -1:
            logger.warning(
                "Refresh token reuse detected. Token family revoked."
            )

        return None

    async def revoke(self, jti: str) -> None:
        """
        Revoga a família associada a um identificador de token,
        ativo ou já consumido.
        """

        await self._redis.eval(
            _REVOKE_BY_JTI_SCRIPT,
            2,
            self._key(jti),
            self._used_key(jti),
        )

    async def revoke_family(self, family_id: str) -> None:
        """
        Revoga atomicamente toda a família de refresh tokens.
        """

        await self._redis.eval(
            _REVOKE_FAMILY_SCRIPT,
            1,
            self._family_key(family_id),
        )