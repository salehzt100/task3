from typing import List

from fastapi import APIRouter

from database.schema import CommentResponse, CommentRequestBody

router = APIRouter(tags=["Comments"])

''' COMMENTS APIs '''
@router.get('/articles/{article_id}/comments', response_model=List[CommentResponse])
async def list_comments(article_id: int):
    pass

@router.post('/articles/{article_id}/comments', response_model=CommentResponse)
async def create_comment(article_id: int, body: CommentRequestBody):
    pass
