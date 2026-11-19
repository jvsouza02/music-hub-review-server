from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class AlbumResponse(BaseModel):
    id: UUID
    mbid: str
    artist_id: UUID
    title: str
    release_date: str
    total_tracks: int
    average_score: float | None
    review_count: int

    model_config = ConfigDict(from_attributes=True)


class AlbumSearchResult(BaseModel):
    mbid: UUID
    title: str
    artist_name: str | None = None
    artist_mbid: UUID | None = None
    release_date: str | None = None
    total_tracks: int | None = None
    average_score: float | None = None
    review_count: int = 0


class AlbumFiltersParams(BaseModel):
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