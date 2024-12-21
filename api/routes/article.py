from datetime import datetime
from typing import  Union, Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends
from app.controllers import ArticleController
from database.schema import ArticleResponse, ArticleRequestBody, ArticleStatus, ArticleFilterType, \
    ArticleUpdateRequestBody

router = APIRouter(tags=["Articles"])

''' ARTICLES APIs '''


@router.get('/articles', tags=["Articles"])
async def list_articles(
    search: Optional[str] = Query(None, description="Search"),
    filter_type: Optional[ArticleFilterType] = Query(None, description="Type of filter"),
    filter_value: Optional[Union[str, ArticleStatus, datetime]] = Query(None, description="Value for the selected filter type"),
    article_controller: ArticleController = Depends()):
    return  article_controller.index(search, filter_type, filter_value)

@router.get('/articles/{article_id}', response_model=ArticleResponse)
async def show_article(article_id: int,article_controller: ArticleController = Depends()):
    return  article_controller.show(article_id)

@router.post('/articles')
async def create_article(article_body: ArticleRequestBody,article_controller:ArticleController =Depends()):
    return  article_controller.store(request=article_body)

@router.put('/articles/{article_id}', response_model=ArticleResponse)
async def update_article(article_id: int, article_body:ArticleUpdateRequestBody  ,article_controller:ArticleController =Depends()):
    return article_controller.update(article_id, article_body)

@router.delete('/articles/{article_id}', response_model=dict)
async def delete_article(article_id: int, article_controller:ArticleController =Depends()):
    return article_controller.destroy(article_id)
