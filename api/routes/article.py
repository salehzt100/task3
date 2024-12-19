from datetime import datetime
from typing import List, Union, Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.controllers import ArticleController
from bootstrap import get_db
from database.schema import  ArticleResponse, ArticleRequestBody, ArticleStatus
from utils.utils import oauth2_scheme

router = APIRouter(tags=["Articles"])

''' ARTICLES APIs '''


@router.get('/articles', response_model=List[ArticleResponse], tags=["Articles"])
async def list_articles(
    search: Optional[str] = Query(None, description="Search"),
    filter_type: Optional[str] = Query(None, description="Type of filter"),
    filter_value: Optional[Union[str, ArticleStatus, datetime]] = Query(
        None, description="Value for the selected filter type"
    ),
):
    pass

@router.get('/articles/{article_id}', response_model=ArticleResponse)
async def show_article(article_id: int):
    pass

@router.post('/articles')
async def create_article(article_body: ArticleRequestBody,article_controller:ArticleController =Depends()):
    return  article_controller.store(request=article_body)

@router.put('/articles/{article_id}', response_model=ArticleResponse)
async def update_article(article_id: int, article_body: ArticleRequestBody):
    pass

@router.delete('/articles/{article_id}', response_model=dict)
async def delete_article(article_id: int):
    pass
