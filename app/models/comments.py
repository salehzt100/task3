from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from app.models import Base, User, Article

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    content: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )
    article_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("articles.id"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationship with the Article
    article: Mapped[Article] = relationship(
        "Article",
        back_populates="comments"
    )
    user: Mapped[User] = relationship(
        "User",
        back_populates="comments"
    )
