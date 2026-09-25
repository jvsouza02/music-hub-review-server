from src.infrastructure.database.base import Base
from src.infrastructure.database.album.model import AlbumModel
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, DateTime, func, UniqueConstraint
from datetime import datetime

class TrackModel(Base):
    __tablename__ = "tracks"
    __table_args__ = (
            UniqueConstraint("album_id", "position", name="uq_album_track_position"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    mbid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    duration_ms: Mapped[int] = mapped_column(nullable=True)
    album_id: Mapped[UUID] = mapped_column(ForeignKey("albums.id"), index=True, nullable=False)
    metadata_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
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

    album: Mapped["AlbumModel"] = relationship()

