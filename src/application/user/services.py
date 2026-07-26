# importar entidade, interface de repositorio, exceptions e security para gerar senha hash
from src.core.security import generate_password_hash
from src.domain.user.entity import User
from src.domain.user.exceptions import EmailAlreadyInUseException
from src.domain.user.repository import IUserRepository

# criar classe de servico de usuario
class UserService:
    # iniciar construtor injetando o repositorio
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    # criar metodo de criação de usuario, que recebe nome, email e senha
    async def create_user(self, username: str, email: str, password: str) -> User:
        # verificamos se o usuario ja existe
        if await self._repository.get_by_email(email):
            # caso exista, lançar a exceção criada
            raise EmailAlreadyInUseException(email=email)

        # gerar senha hasheada
        hashed_password = generate_password_hash(password)

        # instanciar entidade
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

        # salvar no banco de dados
        saved_user = await self._repository.save(new_user)

        # retornar usuario criado
        return saved_user