from pydantic import BaseModel, ConfigDict, Field, EmailStr, StrictBool
from uuid import UUID, uuid4

class User(BaseModel):
    model_config = ConfigDict(
        frozen=True, # Impede que a entidade se torne mutável
        from_attributes=True, # Permite a conversão para modelos SQLAchemy
        str_strip_whitespace=True, # Remove os espaços em branco no inicio e fim das str
    )

    id: UUID = Field(default_factory=uuid4)
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str
    is_active: StrictBool = True