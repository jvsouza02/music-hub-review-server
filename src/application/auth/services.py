from src.domain.user.repository import IUserRepository
from src.domain.user.exceptions import InvalidCredentialsException
from src.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, repository: IUserRepository):
        self._user_repository = repository


    async def authenticate_user(self, email: str, password: str) -> str:
        saved_user = await self._user_repository.get_by_email(email)

        if not saved_user:
            raise InvalidCredentialsException()

        if not verify_password(password, str(saved_user.password)):
            raise InvalidCredentialsException()

        return create_access_token({"sub": str(saved_user.id)})

        

        

        

        

        