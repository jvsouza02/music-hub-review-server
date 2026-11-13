import math
import time
import jwt

from uuid import UUID

from src.domain.user.repository import IUserRepository
from src.domain.user.exceptions import InvalidCredentialsException

from src.core.security import (
    verify_password,
    create_access_token,
    refresh_access_token,
    decode_token,
)

from .refresh_token_store import RefreshTokenStore


class AuthService:
    def __init__(
        self,
        repository: IUserRepository,
        refresh_store: RefreshTokenStore,
    ):
        self._user_repository = repository
        self._refresh_store = refresh_store

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> tuple[str, str, str]:

        saved_user = await self._user_repository.get_by_email(email)

        if not saved_user:
            raise InvalidCredentialsException()

        if not verify_password(password, str(saved_user.password)):
            raise InvalidCredentialsException()

        user_id = str(saved_user.id)

        access = create_access_token({"sub": user_id})

        jti, family_id = await self._refresh_store.create(user_id)

        refresh = refresh_access_token({
            "sub": user_id,
            "jti": jti,
            "family": family_id,
        })

        return access, refresh, jti

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> tuple[str, str, str]:

        # 1. Valida assinatura e expiração do JWT.
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError as exc:
            raise InvalidCredentialsException(
                "Invalid refresh token."
            ) from exc

        # 2. Confere o tipo e a estrutura do token.
        if payload.get("type") != "refresh":
            raise InvalidCredentialsException("Invalid token type.")

        jti = payload.get("jti")
        family_id = payload.get("family")
        subject = payload.get("sub")
        token_exp = payload.get("exp")

        if not all(
            isinstance(value, str) and value
            for value in (jti, family_id, subject)
        ):
            raise InvalidCredentialsException(
                "Invalid refresh token structure."
            )

        if isinstance(token_exp, bool) or not isinstance(
            token_exp,
            (int, float),
        ):
            raise InvalidCredentialsException(
                "Invalid refresh token expiration."
            )

        try:
            user_uuid = UUID(subject)
        except ValueError as exc:
            raise InvalidCredentialsException() from exc

        # O registro consumido deve permanecer somente até
        # a expiração original do refresh token.
        used_ttl = math.ceil(token_exp - time.time())

        if used_ttl <= 0:
            raise InvalidCredentialsException(
                "Refresh token expired."
            )

        # 3. Verifica se o usuário continua existindo.
        saved_user = await self._user_repository.get_by_id(user_uuid)

        if not saved_user:
            raise InvalidCredentialsException()

        # 4. Rotaciona atomicamente o refresh token.
        rotation = await self._refresh_store.validate_and_rotate(
            jti,
            family_id,
            used_ttl,
        )

        if not rotation:
            raise InvalidCredentialsException(
                "Refresh token invalid or reused."
            )

        new_jti, rotated_family_id = rotation

        # 5. Emite os novos tokens.
        new_access = create_access_token({"sub": str(user_uuid)})

        new_refresh = refresh_access_token({
            "sub": str(user_uuid),
            "jti": new_jti,
            "family": rotated_family_id,
        })

        return new_access, new_refresh, new_jti

    async def logout(self, family_id: str | None) -> None:
        if family_id:
            await self._refresh_store.revoke_family(family_id)