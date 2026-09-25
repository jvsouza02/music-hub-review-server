from src.infrastructure.database.base import Base
from src.infrastructure.database.artist.model import ArtistModel
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime, func
from uuid import UUID

class AlbumModel(Base):
    __tablename__ = "albums"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    mbid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    release_date: Mapped[str] = mapped_column(String(10), nullable=True)
    total_tracks: Mapped[int] = mapped_column(nullable=False)
    artist_id: Mapped[UUID] = mapped_column(ForeignKey("artists.id"), index=True, nullable=False)
    metadata_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    artist: Mapped["ArtistModel"] = relationship()

