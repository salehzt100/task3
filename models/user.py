from __future__ import annotations
import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, ForeignKey
from models import Base

if TYPE_CHECKING:
    from models import Article, PersonalAccessToken, Role   # Only import for type checking


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
    role_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("roles.id")
    )


    # Define the relationship with Role

    role: Mapped[Role] = relationship(
        "Role",
        back_populates="users"
    )

    # Define the relationship with PersonalAccessToken
    personal_access_tokens: Mapped[List[PersonalAccessToken]] = relationship(
        "PersonalAccessToken",
        back_populates="users"
    )

    # Define the relationship with Articles
    articles: Mapped[List[Article]] = relationship(
        "Article",
        back_populates="users"
    )
