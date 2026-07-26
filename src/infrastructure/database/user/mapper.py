from src.domain.user.entity import User
from src.infrastructure.database.user.model import UserModel

class UserMapper:
    @staticmethod
    def to_entity(model: UserModel) -> User:
        return User.model_validate(model)


    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(**entity.model_dump())