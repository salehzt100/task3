from datetime import datetime
from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.models import Article
from app.models.articles import ArticleStatus
from app.repositories import ArticleRepository
from app.repositories.article_tags_repository import ArticleTagsRepository
from database.schema import ArticleUpdateRequestBody


class ArticleService:

    def __init__(self, db: Session):
        self.db = db
        self.article_repository = ArticleRepository(db)
        self.article_tag_repository = ArticleTagsRepository(db)

    def create_article(self, request, current_user):
        """
        Create a new article and associate tags with it.
        """
        new_article = Article(
            user_id=current_user.id,
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

    def get_articles(self, search: str = None, filter_type: str = None, filter_value: str = None):
        """
        Retrieve articles based on optional search and filters.
        """
        articles = self.article_repository.select(search, filter_type, filter_value)
        return articles

    def change_status(self, article_id: int, status: str):
        """
        Change the status of an article.
        """
        article = self.article_repository.get_article_py_id(article_id)
        if not article:
            raise NotFoundException(f'Article with id {article_id} not found')

        article.status = ArticleStatus[status]
        self.article_repository.update(article)

        return article

    def draft_article(self, article_id: int):
        """
        Change the status of an article to 'DRAFT'.
        """
        article = self.article_repository.get_article_py_id(article_id)
        if not article:
            raise NotFoundException(f'Article with id {article_id} not found')

        article.status = ArticleStatus.DRAFT
        self.article_repository.update(article)

        return article

    def submit_article(self, article_id: int):
        """
        Change the status of an article to 'SUBMITTED'.
        """
        article = self.article_repository.get_article_py_id(article_id)
        if not article:
            raise NotFoundException(f'Article with id {article_id} not found')

        article.status = ArticleStatus.SUBMITTED
        self.article_repository.update(article)

        return article

    def update_article(self, article_id: int, request: ArticleUpdateRequestBody):
        """
        Update an article and its associated tags.
        """
        article = self.article_repository.get_article_py_id(article_id)

        if request.title is not None:
            article.title = request.title
        if request.body is not None:
            article.body = request.body
        if request.category_id is not None:
            article.category_id = request.category_id

        self.article_repository.update(article=article)

        tags = request.tags
        if tags:
            added_tags = [
                {'article_id': article.id, 'tag_id': tag, 'created_at': datetime.now()}
                for tag in tags if tag not in [tag.id for tag in article.tags]
            ]
            deleted_tags = [tag.id for tag in article.tags if tag.id not in tags]

            if added_tags:
                self.article_tag_repository.create(added_tags)
            if deleted_tags:
                self.article_tag_repository.delete(article_id, deleted_tags)

        return article
