from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Article
from app.models.articles import ArticleStatus
from app.repositories import ArticleRepository
from app.repositories.article_tags_repository import ArticleTagsRepository
from database.schema import ArticleRequestBody


class ArticleService:

    def __init__(self, db: Session):
        self.db = db
        self.article_repository = ArticleRepository(db)
        self.article_tag_repository = ArticleTagsRepository(db)

    def create_article(self, request: ArticleRequestBody):

        new_article = Article(
            user_id=request.user_id,
            title=request.title,
            body=request.body,
            status=ArticleStatus.DRAFT,
            category_id=request.category_id,
            created_at=datetime.now(),
        )

        article= self.article_repository.insert( new_article)

        article_tags=[
            {'article_id':article.id, 'tag_id':tag_id, 'created_at':datetime.now()}
            for tag_id in request.tags
        ]

        self.article_tag_repository.create( article_tags)

        return article






