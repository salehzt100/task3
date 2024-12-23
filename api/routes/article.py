from datetime import datetime
from typing import  Union, Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends
from app.controllers import ArticleController
from app.models import User
from database.schema import ArticleResponse, ArticleRequestBody, ArticleStatus, ArticleFilterType, \
    ArticleUpdateRequestBody
from utils import  get_current_user
from utils.fastapi.dependencies import role_required

router = APIRouter( tags=["Articles"])

''' ARTICLES APIs '''

@router.get(
    '/articles',
    tags=["Articles"],
    summary="List all articles",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def list_articles(
    search: Optional[str] = Query(None, description="Search for articles by keyword."),
    filter_type: Optional[ArticleFilterType] = Query(None, description="Type of filter to apply."),
    filter_value: Optional[Union[str, ArticleStatus, datetime]] = Query(None, description="Value for the selected filter type."),
    article_controller: ArticleController = Depends()
):
    """
    List all articles with optional filters and search.
    """
    return article_controller.index(search, filter_type, filter_value)


@router.get(
    '/articles/{article_id}',
    response_model=ArticleResponse,
    summary="Show a specific article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def show_article(
    article_id: int,
    article_controller: ArticleController = Depends()
):
    """
    Get details of an article by its ID.
    """
    return article_controller.show(article_id)


@router.post(
    '/articles',
    summary="Create a new article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def create_article(
    article_body: ArticleRequestBody,
    current_user: User = Depends(get_current_user),
    article_controller: ArticleController = Depends()
):
    """
    Create a new article.
    """
    return article_controller.store(request=article_body, current_user=current_user)


@router.put(
    '/articles/{article_id}',
    response_model=ArticleResponse,
    summary="Update an existing article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def update_article(
    article_id: int,
    article_body: ArticleUpdateRequestBody,
    article_controller: ArticleController = Depends()
):
    """
    Update an article by its ID.
    """
    return article_controller.update(article_id, article_body)


@router.delete(
    '/articles/{article_id}',
    response_model=dict,
    summary="Delete a specific article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def delete_article(
    article_id: int,
    article_controller: ArticleController = Depends()
):
    """
    Delete an article by its ID.
    """
    return article_controller.destroy(article_id)


@router.patch(
    '/articles/{article_id}/submit',
    response_model=ArticleResponse,
    summary="Submit an article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def submit_article(
    article_id: int,
    article_controller: ArticleController = Depends()
):
    """
    Submit an article for review or publication.
    """
    return article_controller.submit(article_id)


@router.patch(
    '/articles/{article_id}/draft',
    response_model=ArticleResponse,
    summary="Draft an article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def draft_article(
    article_id: int,
    article_controller: ArticleController = Depends()
):
    """
    Move an article back to draft status.
    """
    return article_controller.draft(article_id)


@router.patch(
    '/articles/{article_id}/status',
    response_model=ArticleResponse,
    summary="Change the status of an article",
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def change_article_status(
    article_id: int,
    new_status: ArticleStatus,
    article_controller: ArticleController = Depends()
):
    """
    Change the status of an article.
    """
    return article_controller.change_status(article_id, new_status)
