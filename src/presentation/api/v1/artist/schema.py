from pydantic import BaseModel, ConfigDict
from fastapi import Query
from uuid import UUID
from decimal import Decimal
from typing import Annotated

class ArtistResponse(BaseModel):
    id: UUID
    mbid: str
    name: str
    disambiguation: str | None = None
    country: str | None = None
    average_score: Decimal | None = None
    review_count: int

    model_config = ConfigDict(from_attributes=True)


class ArtistFiltersParams(BaseModel):
    limit: Annotated[
        int,
        Query(ge=1, le=100, description="Quantidade de itens")
    ] = 20,
    offset: Annotated[
        int,
        Query(ge=0, description="Pular X itens")
    ] = 0,