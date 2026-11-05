from pydantic import BaseModel, ConfigDict
from uuid import UUID
from decimal import Decimal
from typing import Annotated
from fastapi import Query

class TrackResponse(BaseModel):
    id: UUID
    mbid: str
    album_id: UUID
    title: str
    position: int
    duration_ms: int | None
    avegare_score: Decimal | None
    review_count: int

    model_config = ConfigDict(from_attributes=True)


class TrackFiltersParams(BaseModel):
    limit: Annotated[
        int,
        Query(ge=1, le=100, description="Quantidade de itens")
    ] = 20,
    offset: Annotated[
        int,
        Query(ge=0, description="Pular X itens")
    ] = 0,