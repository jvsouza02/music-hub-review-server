from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class ArtistResponse(BaseModel):
    id: UUID
    mbid: str
    name: str
    disambiguation: str | None = None
    country: str | None = None
    average_score: float | None = None
    review_count: int

    model_config = ConfigDict(from_attributes=True)


class ArtistFiltersParams(BaseModel):
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