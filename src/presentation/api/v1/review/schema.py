from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Any
from uuid import UUID
from datetime import datetime

class ReviewCreateRequest(BaseModel):
    track_mbid: Annotated[str, Field(min_length=36, max_length=36)]
    score: Annotated[float, Field(ge=0.5, le=5.0, multiple_of=0.5)]
    body: Annotated[str | None, Field(max_length=5000)] = None

class ReviewUpdateRequest(BaseModel):
    new_score_value: Annotated[float | None, Field(ge=0.5, le=5.0, multiple_of=0.5)] = None
    new_body: Annotated[str | None, Field(max_length=5000)] = None

class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    track_id: UUID
    score: float
    body: str | None
    created_at: datetime |  None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("score", mode="before")
    @classmethod
    def extract_score_value(cls, v: Any) -> float:
        if hasattr(v, "value"):
            return float(v.value)
        return float(v)


class ReviewFiltersParams(BaseModel):
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Quantidade de itens"
    )

    offset: int = Field(
        default=0,
        ge=0,
        description="Pular X itens"
    )