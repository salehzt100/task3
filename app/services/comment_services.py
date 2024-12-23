from datetime import datetime

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.models import Comment
from app.repositories import ArticleRepository
from app.repositories.comment_repository import CommentRepository
from database.schema import CommentUpdateRequestBody


class CommentService:
    def __init__(self,db: Session):
        self.db = db
        self.article_repository = ArticleRepository(db)
        self.comment_repository = CommentRepository(db)



    def get_comments(self,article_id):
        article = self.article_repository.get_article_py_id(article_id)
        return article.comments
    def add_comment(self,article_id,request,current_user):

        new_comment = Comment(
            article_id=article_id,
            content=request.content,
            user_id=current_user.id,
            created_at=datetime.now(),
        )

        article = self.comment_repository.insert(new_comment)
        return article

    def update_comment(self,comment_id,request: CommentUpdateRequestBody ):
         comment = self.comment_repository.get_comment_by_id(comment_id)
         if request.content:
            comment.content = request.content
            self.comment_repository.update(comment)

         return comment

    def delete_comment(self,comment_id):
        comment = self.comment_repository.get_comment_by_id(comment_id)
        if not comment:
            raise NotFoundException(f'Comment with id {comment_id} not found')

        return self.comment_repository.delete(comment)