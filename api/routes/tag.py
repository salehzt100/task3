from typing import List

from fastapi import APIRouter

from database.schema import  TagResponse, TagRequestBody

router = APIRouter(tags=["Tags"])


''' TAGS APIs '''
@router.get('/tags', response_model=List[TagResponse])
async def list_tags():
    pass

@router.get('/tags/{tags_id}', response_model=TagResponse)
async def show_tag(tags_id: int):
    pass

@router.post('/tags', response_model=TagResponse)
async def create_tag(tag_body: TagRequestBody):
    pass

@router.put('/tags/{tag_id}', response_model=TagResponse)
async def update_tag(tag_id: int, tag_body: TagRequestBody):
    pass

@router.delete('/tags/{tag_id}', response_model=dict)
async def delete_tag(tag_id: int):
    pass
