from src.infrastructure.database.base import Base
from src.infrastructure.database.user.model import User
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, ForeignKey, Numeric, Text, DateTime, func
from decimal import Decimal
from uuid import UUID
from datetime import datetime

class ReviewModel(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "track_id", name="uq_review_user_track")
    )

    review_id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    track_id: Mapped[UUID] = mapped_column(ForeignKey("track.id"), index=True, nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=True)
    is_edited: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user: Mapped["User"] = relationship()

