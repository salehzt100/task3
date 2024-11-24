from sqlalchemy import Table, ForeignKey, Integer, DateTime, func
from sqlalchemy import Column
from models import Base

article_tag = Table(
    'article_tag',
    Base.metadata,
    Column(
        'article_id',
        Integer, ForeignKey('articles.id'),
        primary_key=True
    ),
    Column('tag_id',
           Integer, ForeignKey('tags.id'),
           primary_key=True
           ),
    Column('created_at',
           DateTime(timezone=True),
           default=func.now(),
           nullable=False
           ),
)


