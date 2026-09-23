from datetime import datetime, timedelta, timezone
from uuid import uuid4, UUID
from pydantic import BaseModel, ConfigDict, Field

class Album(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        str_strip_whitespace=True
    )

    id: UUID = Field(default_factory=uuid4)
    mbid: str = Field(min_length=36, max_length=36)
    artist_id: UUID
    title: str = Field(
        min_length=1,
        max_length=255,
        examples=["Meteora", "The Death of Peace of Mind"]
    )
    release_date: str | None = Field(
        default=None,
        description="Formato ISO YYYY-MM-DD ou YYYY"
    )
    total_tracks: int = Field(ge=1)
    metadata_updated_at = datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    def is_stale(self, ttl_days: int = 30) -> bool:
            expiration_date = self.metadata_updated_at + timedelta(days=ttl_days)
            return datetime.now(timezone.utc) > expiration_date
