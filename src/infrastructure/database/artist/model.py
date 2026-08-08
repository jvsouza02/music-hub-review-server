from uuid import UUID
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.base import Base
from datetime import datetime

class ArtistModel(Base):
    __tablename__ = "artists"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True
    )

    mbid: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    disambiguation: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True 
    )

    country: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )
    
    metadata_updated_at:  Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

