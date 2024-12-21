from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Article
from app.models.articles import ArticleStatus
from app.repositories import ArticleRepository
from app.repositories.article_tags_repository import ArticleTagsRepository
from database.schema import ArticleRequestBody, ArticleUpdateRequestBody


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

        article = self.article_repository.insert(new_article)

        article_tags = [
            {'article_id': article.id, 'tag_id': tag_id, 'created_at': datetime.now()}
            for tag_id in request.tags
        ]

        self.article_tag_repository.create(article_tags)

        return article

    def get_articles(self, search: None | str = None, filter_type: None | str = None, filter_value: None | str = None):
        articles = self.article_repository.select(search, filter_type, filter_value)
        return articles

    def update_article(self, article_id: int, request: ArticleUpdateRequestBody):

        article = self.article_repository.get_article_py_id(article_id)

        if request.title is not None:
            article.title = request.title,
        if request.body is not None:
            article.body = request.body,
        if request.category_id is not None:
            article.category_id = request.category_id,

        self.article_repository.update(article=article)
        tags = request.tags
        if tags:

            t = [tag.id for tag in article.tags]
            print('article tags', article.tags, 't:   ', t)
            added_tags = [
                {'article_id': article.id, 'tag_id': tag, 'created_at': datetime.now()}
                for tag in tags if tag not in [tag.id for tag in article.tags]
            ]

            deleted_tags = [
                tag.id for tag in article.tags if tag.id not in tags
            ]
            if added_tags:
                print('added_tags: ', added_tags)
                self.article_tag_repository.create(added_tags)
            if deleted_tags:
                print('deleted_tags: ', deleted_tags)
                self.article_tag_repository.delete(article_id, deleted_tags)

        return article
