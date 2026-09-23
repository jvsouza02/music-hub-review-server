from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import timezone, timedelta, datetime

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
    metadata_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def is_stale(self, ttl_days: int = 30) -> bool:
                expiration_date = self.metadata_updated_at + timedelta(days=ttl_days)
                return datetime.now(timezone.utc) > expiration_date