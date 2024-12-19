from fastapi import Depends
from sqlalchemy.orm import Session

from app.services import ArticleService
from bootstrap import get_db
from database.schema import ArticleRequestBody, ArticleResponse, UserResponseModel, UserResponse, CategoryResponseModel, \
    TagResponseModel
from utils import exception_handler


class ArticleController:

    def __init__(self,  db: Session = Depends(get_db)):
        self.db = db
        self.article_service = ArticleService(db)

    @exception_handler
    def store(self, request: ArticleRequestBody):


        article =  self.article_service.create_article(request)
        return ArticleResponse(
            id = article.id,
            title = article.title,
            body = article.body,
            created_at=article.created_at,
            status=article.status.name,
            user=UserResponse(
                id = article.user.id,
                name = article.user.name,
                role = article.user.role.name,
            ),
            category=CategoryResponseModel(
                id = article.category.id,
                name = article.category.name,
                created_at=article.category.created_at,
            ),
            tags=[TagResponseModel(
                id = tag.id,
                name = tag.name,
                created_at=tag.created_at,
            )
            for tag in article.tags
            ],
        )


