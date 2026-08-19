from src.infrastructure.database.base import Base
from uuid import UUID
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.user.entity import UserRole

class UserModel(Base):
    __tablename__  = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(SQLEnum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    