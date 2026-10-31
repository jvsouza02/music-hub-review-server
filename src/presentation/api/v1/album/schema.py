from pydantic import BaseModel, ConfigDict
from fastapi import Query
from typing import Annotated
from uuid import UUID
from decimal import Decimal

class AlbumResponse(BaseModel):
    id: UUID
    mbid: str
    artist_id: UUID
    title: str
    release_date: str
    total_tracks: int
    avegare_score: Decimal | None
    review_count: int

    model_config = ConfigDict(from_attributes=True)

class AlbumFiltersParams(BaseModel):
    limit: Annotated[
        int,
        Query(ge=1, le=100, description="Quantidade de itens")
    ] = 20,
    offset: Annotated[
        int,
        Query(ge=0, description="Pular X itens")
    ] = 0,