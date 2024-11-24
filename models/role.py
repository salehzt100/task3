from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func

from models import Base, role_permission, Permission, User


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
        back_populates="roles"
    )


    # Relationship with Users
    users: Mapped[List[User]] = relationship(
        "User",
        back_populates="role"
    )
