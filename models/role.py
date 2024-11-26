from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func

from models import Base
from models.role_permission import role_permission

if TYPE_CHECKING:
    from models import Permission, User  # Only import for type checking

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    permissions: Mapped[List[Permission]] = relationship(
        "Permission",
        secondary=role_permission,
    )


    # Relationship with Users
    users: Mapped[List[User]] = relationship(
        "User",
        back_populates="role"
    )
