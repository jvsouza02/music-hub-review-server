from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Any
from uuid import UUID
from datetime import datetime

class ReviewCreateRequest(BaseModel):
    track_mbid: Annotated[str, Field(min_length=36, max_length=36)]
    score: Annotated[float, Field(ge=0.5, le=5.0)]
    body: str | None = None

class ReviewResponse(BaseModel):
    review_id: UUID
    user_id: UUID
    track_id: UUID
    score: float
    body: str | None
    created_at: datetime |  None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator
    @classmethod
    def extract_score_value(cls, v: Any) -> float:
        if hasattr(v, "value"):
            return float(v.value)
        return float(v)