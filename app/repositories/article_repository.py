from sqlalchemy.orm import Session

from app.models import Article


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db


    def insert(self, article: Article):
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

