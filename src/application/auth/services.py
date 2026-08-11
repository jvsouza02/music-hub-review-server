from src.domain.user.repository import IUserRepository
from src.domain.user.exceptions import InvalidCredentialsException
from src.core.security import (verify_password, create_access_token, 
refresh_access_token, decode_token)
from .refresh_token_store import RefreshTokenStore
from uuid import UUID

class AuthService:
    def __init__(
        self,
        repository: IUserRepository,
        refresh_store: RefreshTokenStore
    ):
        self._user_repository = repository
        self._refresh_store = refresh_store


    async def authenticate_user(self, email: str, password: str) -> str:
        saved_user = await self._user_repository.get_by_email(email)

        if not saved_user:
            raise InvalidCredentialsException()

        if not verify_password(password, str(saved_user.password)):
            raise InvalidCredentialsException()

        user_id: str = str(saved_user.id)

        access = create_access_token({"sub": user_id})

        jti, family_id = await self._refresh_store.create(user_id)
        refresh = create_access_token({
            "sub": user_id,
            "jti": jti,
            "family": family_id
        })

        return access, refresh, jti


    async def refresh_access_token(self, refresh_token: str) -> str:
        decoded_token = decode_token(refresh_token)

        if decoded_token.get("type") != "refresh":
            raise InvalidCredentialsException("Invalid token type.")

        jti = decoded_token.get("jti")
        family_id = decoded_token.get("family")
        if not jti or not family_id:
            raise InvalidCredentialsException("Invalid refresh token structure")

        result = await self._refresh_store.validate_and_rotate(jti)
        if not result:
            raise InvalidCredentialsException("Refresh token invalid or reused")

        new_jti, _ = result

        user_id = decoded_token.get("sub")
        if not user_id:
            raise InvalidCredentialsException()

        saved_user = self._user_repository.get_by_id(UUID(user_id))
        if not saved_user:
             raise InvalidCredentialsException()

        new_access = create_access_token({"sub": user_id})
        new_refresh = refresh_access_token({
            "sub": user_id,
            "jti": new_jti,
            "family": family_id
        })

        return new_access, new_refresh, new_jti


    async def logout(self, refresh_jti: str | None) -> None:
        if refresh_jti:
            await self._refresh_store.revoke(refresh_jti)