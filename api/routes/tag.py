from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.controllers.tag_controller import TagController
from bootstrap import get_db
from database.schema import TagResponse, TagRequestBody, tag_as_form, TagResponseModel, TagsResponse

router = APIRouter(tags=["Tags"])

''' TAGS APIs '''
@router.get('/tags', response_model=TagsResponse)
async def list_tag(search: str | None = Query(None), db: Session = Depends(get_db)):
    return TagController.index(search, db)

@router.get('/tags/{tag_id}', response_model=TagResponseModel)
async def show_tag(tag_id, db: Session = Depends(get_db)):
    return TagController.show(tag_id, db)

@router.post('/tags', response_model=TagResponse)
async def create_tag(request: TagRequestBody = Depends(tag_as_form), db: Session = Depends(get_db)):
    return TagController.store(request, db)

@router.delete('/tags/{tag_id}', response_model=dict)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    return TagController.destroy(tag_id, db)

@router.put('/tags/{tag_id}', response_model=TagResponse)
async def update_tag(tag_id: int, tag_body: TagRequestBody, db: Session = Depends(get_db)):
    return TagController.update(tag_id, tag_body, db)
