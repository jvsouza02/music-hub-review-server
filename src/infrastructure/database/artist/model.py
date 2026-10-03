from uuid import UUID
from sqlalchemy import String, DateTime, func, Numeric
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.base import Base
from datetime import datetime

class ArtistModel(Base):
    __tablename__ = "artists"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    mbid: Mapped[str] = mapped_column(
        String(36),
        unique=True,
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

    average_score: Mapped[Decimal | None] = mapped_column(
        Numeric(2, 1), nullable=True
    )

    review_count: Mapped[int] = mapped_column(
        server_default="0",
        nullable=False
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
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

