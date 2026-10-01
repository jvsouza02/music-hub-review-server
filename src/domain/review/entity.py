from pydantic import BaseModel, ConfigDict, Field
from src.domain.music.value_objects.score import Score
from uuid import UUID, uuid4
from datetime import datetime

class Review(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        str_strip_whitespace=True
    )

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    track_id: UUID
    score: Score
    body: str | None = Field(default=None, max_length=5000)
    is_active: bool = True
    is_edited: bool = False
    created_at: datetime | None
    updated_at: datetime | None

