from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.comment_services import CommentService
from bootstrap import get_db
from database.schema import CommentRequestBody, CommentResponse, UserResponse
from utils import exception_handler


class CommentController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.comment_service = CommentService(db)

    @exception_handler
    def store(self, article_id: int, request: CommentRequestBody, current_user):
        """
        Add a comment to an article.
        """
        article = self.comment_service.add_comment(article_id, request, current_user)
        return self.comment_response(article)

    @exception_handler
    def index(self, article_id: int):
        """
        Retrieve all comments for a given article.
        """
        comments = self.comment_service.get_comments(article_id)
        return [self.comment_response(comment) for comment in comments]

    @exception_handler
    def update(self, comment_id: int, request: CommentRequestBody):
        """
        Update a comment by its ID.
        """
        comment = self.comment_service.update_comment(comment_id, request)
        return self.comment_response(comment)

    @exception_handler
    def destroy(self, comment_id: int):
        """
        Delete a comment by its ID.
        """
        self.comment_service.delete_comment(comment_id)
        return {'success': True, 'message': 'Comment deleted'}

    @exception_handler
    def comment_response(self, comment):
        """
        Generate a response model for a comment.
        """
        return CommentResponse(
            id=comment.id,
            content=comment.content,
            article_id=comment.article_id,
            user=UserResponse(
                id=comment.user.id,
                name=comment.user.name,
                role=comment.user.role.name,
            ),
            created_at=comment.created_at,
        )
