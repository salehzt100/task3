from typing import List

from fastapi import APIRouter, Depends

from app.controllers.comment_controller import CommentController
from app.models import User
from database.schema import CommentResponse, CommentRequestBody, CommentUpdateRequestBody
from utils import get_current_user
from utils.fastapi.dependencies import role_required

router = APIRouter(tags=["Comments"])

# COMMENTS APIs

@router.get(
    '/articles/{article_id}/comments',
    response_model=List[CommentResponse],
    dependencies=[Depends(role_required(['ADMIN']))],
    summary="List all comments for an article"
)
async def list_comments(
    article_id: int,
    comment_controller: CommentController = Depends(CommentController)
):
    """
    Retrieves a list of comments for a specific article.
    """
    return comment_controller.index(article_id)


@router.post(
    '/articles/{article_id}/comments',
    response_model=CommentResponse,
    dependencies=[Depends(role_required(['ADMIN']))],
    summary="Create a comment for an article"
)
async def create_comment(
    article_id: int,
    body: CommentRequestBody,
    current_user: User = Depends(get_current_user),
    comment_controller: CommentController = Depends(CommentController)
):
    """
    Creates a new comment for a specific article by an authenticated user.
    """
    return comment_controller.store(article_id, body, current_user=current_user)


@router.put(
    '/comments/{comment_id}',
    response_model=CommentResponse,
    dependencies=[Depends(role_required(['ADMIN']))],
    summary="Update an existing comment"
)
async def update_comment(
    comment_id: int,
    body: CommentUpdateRequestBody,
    comment_controller: CommentController = Depends(CommentController)
):
    """
    Updates an existing comment by its ID.
    """
    return comment_controller.update(comment_id, body)


@router.delete(
    '/comments/{comment_id}',
    response_model=dict,
    dependencies=[Depends(role_required(['ADMIN']))],
    summary="Delete a comment"
)
async def delete_comment(
    comment_id: int,
    comment_controller: CommentController = Depends(CommentController)
):
    """
    Deletes a comment by its ID.
    """
    return comment_controller.destroy(comment_id)
