from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import timezone, timedelta, datetime
from decimal import Decimal

class Track(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        str_strip_whitespace=True
    )

    id: UUID = Field(default_factory=uuid4)
    mbid: str = Field(min_length=36, max_length=36)
    album_id: UUID
    title: str = Field(
        min_length=1,
        max_length=255,
        examples=["Faint", "Rotten Apple"]
    )
    position: int = Field(
        ge=1,
        description="Track number on the album"
    )
    duration_ms: int | None = Field(
        default=None,
        ge=0,
        description="Track duration (milliseconds)"
    )
    avegare_score: Decimal | None = Field(default=None, ge=0.0, le=5.0)
    review_count: int = Field(default=0, ge=0)
    metadata_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def is_stale(self, ttl_days: int = 30) -> bool:
                expiration_date = self.metadata_updated_at + timedelta(days=ttl_days)
                return datetime.now(timezone.utc) > expiration_date