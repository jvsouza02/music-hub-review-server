from pydantic import BaseModel, ConfigDict, Field, EmailStr, StrictBool
from uuid import UUID, uuid4
from enum import Enum

class UserRole(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(BaseModel):
    model_config = ConfigDict(
        frozen=True, # Impede que a entidade se torne mutável
        from_attributes=True, # Permite a conversão para modelos SQLAchemy
        str_strip_whitespace=True, # Remove os espaços em branco no inicio e fim das str
    )

    id: UUID = Field(default_factory=uuid4)
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER
    is_active: StrictBool = True