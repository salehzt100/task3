from fastapi import Depends
from sqlalchemy.orm import Session

from bootstrap import get_db
from app.exceptions import NotFoundException
from app.models import Article
from app.repositories import ArticleRepository
from app.services import ArticleService
from utils import exception_handler
from database.schema import (
    ArticleResponse,
    UserResponse,
    CategoryResponseModel,
    TagResponseModel,
    ArticleUpdateRequestBody,
    CommentResponseModel,
    ArticleStatus
)


class ArticleController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.article_service = ArticleService(db)
        self.article_repository = ArticleRepository(db)

    @exception_handler
    def store(self, request, current_user):
        article = self.article_service.create_article(request=request, current_user=current_user)
        return self.article_response(article)

    @exception_handler
    def submit(self, article_id: int):
        article = self.article_service.submit_article(article_id)
        return self.article_response(article)

    @exception_handler
    def change_status(self, article_id: int, status: ArticleStatus):
        article = self.article_service.change_status(article_id, status)
        return self.article_response(article)

    @exception_handler
    def draft(self, article_id: int):
        article = self.article_service.draft_article(article_id)
        return self.article_response(article)

    @exception_handler
    def index(self, search: None | str = None, filter_type: None | str = None, filter_value: None | str = None):
        filtered_articles = self.article_service.get_articles(search, filter_type, filter_value)
        return [self.article_response(article) for article in filtered_articles]

    @exception_handler
    def show(self, article_id: int):
        article = self.article_repository.get_article_py_id(article_id)
        return self.article_response(article)

    @exception_handler
    def update(self, article_id: int, request: ArticleUpdateRequestBody):
        article = self.article_service.update_article(article_id, request)
        return self.article_response(article)

    @exception_handler
    def destroy(self, article_id: int):
        article = self.article_repository.get_article_py_id(article_id)
        if article is None:
            raise NotFoundException(f'Article with {article_id} not found ')
        self.article_repository.delete(article)
        return {'success': True, 'message': f'Article with {article_id} deleted successfully'}

    @exception_handler
    def article_response(self, article: Article) -> ArticleResponse:
        return ArticleResponse(
            id=article.id,
            title=article.title,
            body=article.body,
            created_at=article.created_at,
            status=article.status.name,
            user=UserResponse(
                id=article.user.id,
                name=article.user.name,
                role=article.user.role.name,
            ),
            category=CategoryResponseModel(
                id=article.category.id,
                name=article.category.name,
                created_at=article.category.created_at,
            ),
            tags=[TagResponseModel(
                id=tag.id,
                name=tag.name,
                created_at=tag.created_at,
            ) for tag in article.tags],
            comments=[CommentResponseModel(
                id=comment.id,
                content=comment.content,
                user=UserResponse(
                    id=comment.user.id,
                    name=comment.user.name,
                    role=comment.user.role.name,
                ),
                created_at=comment.created_at,
            ) for comment in article.comments],
        )
