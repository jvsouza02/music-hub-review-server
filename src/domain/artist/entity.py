from datetime import timezone, timedelta, datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Artist(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    mbid: str = Field(min_length=36, max_length=36)
    name: str = Field(min_length=1, max_length=255)
    disambiguation: str | None = Field(default=None, max_length=500)
    country: str | None = Field(default=None, max_length=10)
    metadata_updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def is_stale(self, ttl_days: int = 30) -> bool:
        expiration_date = self.metadata_updated_at + timedelta(days=ttl_days)
        return datetime.now(timezone.utc) > expiration_date


    def refresh_metadata(
            self, name: str, disambiguation: str | None, country: str | None,  
    ) -> None:
        self.name = name
        self.disambiguation = disambiguation
        self.country = country
        self.metadata_updated_at =  datetime.now(timezone.utc)