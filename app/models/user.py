from __future__ import annotations
import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, ForeignKey
from app.models import Base

if TYPE_CHECKING:
    from app.models import Article, Role   # Only import for type checking


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id")
    )



    # Define the relationship with Role

    role: Mapped[Role] = relationship(
        "Role",
        back_populates="users"
    )

    # Define the relationship with PersonalAccessToken
    personal_access_tokens = relationship(
        "PersonalAccessToken",
        back_populates="user"
    )

    # Define the relationship with Articles
    articles: Mapped[List[Article]] = relationship(
        "Article",
        back_populates="user"
    )
