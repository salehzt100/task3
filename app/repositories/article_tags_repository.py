from typing import List

from sqlalchemy.orm import Session

from app.models.article_tag import article_tag


class ArticleTagsRepository:
    def __init__(self, db: Session):
        self.db = db


    def create(self, article_tags: List[dict]):
        self.db.execute(article_tag.insert(), article_tags)

