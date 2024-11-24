from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from models import Base, Article



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

    # Relationship with the Article
    article: Mapped[Article] = relationship(
        "Article",
        back_populates="comments"
    )
