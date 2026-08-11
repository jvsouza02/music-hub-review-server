import logging
from uuid import uuid4

from src.infrastructure.cache.redis_client import RedisClient

logger = logging.getLogger(__name__)


class RefreshTokenStore:
    """
    Armazena refresh tokens no Redis com rotação.
    Cada token tem um family_id que identifica a "sessão" do usuário.
    Quando um token é rotacionado, o antigo é invalidado.
    """

    def __init__(self, redis: RedisClient):
        self._redis = redis
        self._ttl_days = 7
        self._ttl_seconds = self._ttl_days * 24 * 3600

    def _key(self, jti: str) -> str:
        return f"refresh:{jti}"

    def _family_key(self, family_id: str) -> str:
        return f"refresh_family:{family_id}"

    async def create(self, user_id: str) -> tuple[str, str]:
        """
        Cria um novo refresh token.
        Retorna (token_jti, family_id).
        """
        jti = str(uuid4())
        family_id = str(uuid4())

        await self._redis.set(
            self._key(jti),
            family_id,
            ttl=self._ttl_seconds,
        )
        await self._redis.set(
            self._family_key(family_id),
            jti,
            ttl=self._ttl_seconds,
        )

        logger.debug(f"Refresh token created: jti={jti}, family={family_id}")
        return jti, family_id

    async def validate_and_rotate(self, jti: str) -> tuple[str, str] | None:
        """
        Valida um refresh token e o rotaciona.
        Retorna (novo_jti, family_id) se válido, None se inválido.
        """
        family_id = await self._redis.get(self._key(jti))
        if not family_id:
            logger.warning(f"Refresh token not found or expired: jti={jti}")
            return None

        # Verifica se este jti é o atual da family
        current_jti = await self._redis.get(self._family_key(family_id))
        if current_jti != jti:
            # Token reutilizado — possível ataque de replay
            logger.error(f"Refresh token replay detected! family={family_id}")
            await self._revoke_family(family_id)
            return None

        # Invalida o token antigo
        await self._redis.delete(self._key(jti))

        # Cria novo token na mesma family
        new_jti = str(uuid4())
        await self._redis.set(
            self._key(new_jti),
            family_id,
            ttl=self._ttl_seconds,
        )
        await self._redis.set(
            self._family_key(family_id),
            new_jti,
            ttl=self._ttl_seconds,
        )

        logger.debug(f"Refresh token rotated: {jti} -> {new_jti}")
        return new_jti, family_id

    async def revoke(self, jti: str) -> None:
        """Invalida um único refresh token."""
        await self._redis.delete(self._key(jti))
        logger.debug(f"Refresh token revoked: jti={jti}")

    async def revoke_family(self, family_id: str) -> None:
        """Invalida toda a sessão (logout de todos os dispositivos)."""
        await self._revoke_family(family_id)

    async def _revoke_family(self, family_id: str) -> None:
        current_jti = await self._redis.get(self._family_key(family_id))
        if current_jti:
            await self._redis.delete(self._key(current_jti))
        await self._redis.delete(self._family_key(family_id))
        logger.info(f"Refresh family revoked: {family_id}")