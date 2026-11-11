from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Annotated
from fastapi import Query

class TrackResponse(BaseModel):
    id: UUID
    mbid: str
    album_id: UUID
    title: str
    position: int
    duration_ms: int | None
    average_score: float | None
    review_count: int

    model_config = ConfigDict(from_attributes=True)

class TrackSearchResult(BaseModel):
    mbid: UUID
    title: str
    artist_name: str
    album_title: str | None
    average_score: float | None
    review_count: int | None

class TrackFiltersParams(BaseModel):
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