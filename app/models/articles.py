from __future__ import annotations
import enum
import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Text, Enum, UUID

from app.models import Base

if TYPE_CHECKING:
    from app.models import   Category, User, Comment, Tag



class ArticleStatus(enum.Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    REJECTED = "rejected"
    SUBMITTED= "SUBMITTED"


class Article(Base):
    __tablename__ = "articles"



    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    title: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    status: Mapped[ArticleStatus] = mapped_column(
        Enum(ArticleStatus, name="status"),
        nullable=False,
        server_default="DRAFT"
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    # Relationship with the Article
    category: Mapped[Category] = relationship(
        "Category",
        back_populates="articles"
    )


    # Relationship with the Article
    user: Mapped[User] = relationship(
        "User", back_populates="articles"
    )


    # Relationship with the Article
    comments: Mapped[List[Comment]] = relationship(
        "Comment",
        back_populates="article"
    )

    # Relationship with the Article

    tags: Mapped[List[Tag]] = relationship(
        "Tag", secondary="article_tag",
        back_populates="articles"
    )

