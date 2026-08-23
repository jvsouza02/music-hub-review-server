from pydantic import BaseModel, Field, model_validator, ConfigDict
from src.domain.music.exceptions import InvalidScoreException
from typing import Annotated
from decimal import Decimal

class Score(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Annotated[Decimal, Field(ge=Decimal("0.5"), le=Decimal("5.0"))]

    @model_validator(mode="after")
    def validate_step(self) -> "Score":
        if (self.value * 2) % 1 != 0:
            raise InvalidScoreException("Score must be a multiple of 0.5")
        return self


    def __str__(self) -> str:
        return str(self.value)


    @classmethod
    def from_float(cls, value: float) -> "Score":
        return Score(value=Decimal(str(value)))
