from datetime import datetime
from operator import or_
from sqlalchemy.sql import func

from sqlalchemy.orm import Session

from app.models import Article, User
from database.schema import ArticleFilterType, ArticleStatus


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert(self, article: Article):
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def select(self, search: str | None = None, filter_type: str | None = None, filter_value: str | None = None):
        query = self.db.query(Article)

        if search:
            query = query.filter(or_(
                Article.title.ilike(f'%{search}%'),
                Article.body.ilike(f'%{search}%')
            ))

        if filter_type and filter_value:
            filter_type = filter_type.casefold()
            if filter_type == ArticleFilterType.DATE.value:

                try:
                    filter_value_date = datetime.strptime(filter_value, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError(f"Invalid date format: {filter_value}. Valid format is 'yyyy-mm-dd'.")

                query = query.filter(func.date(Article.created_at) == filter_value_date)


            elif filter_type == ArticleFilterType.STATUS.value:
                if str.upper(filter_value) not in ArticleStatus._value2member_map_:
                    raise ValueError(
                        f'invalid status: ( {filter_value} ) . Valid statuses : {ArticleStatus._value2member_map_.values()} ')
                query = query.where(Article.status == str.upper(filter_value))

            elif filter_type == ArticleFilterType.AUTHOR.value:
                query = query.join(Article.user).filter(User.name.like(f'{filter_value}%'))

        return query.all()

    def get_article_py_id(self, article_id: int) -> Article:
        return self.db.query(Article).filter(Article.id == article_id).first()

    def update(self, article: Article):
        self.db.commit()
        self.db.refresh(article)

    def delete(self, article: Article):
        self.db.delete(article)
        self.db.commit()

