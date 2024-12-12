
from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.controllers.category_controller import CategoryController
from bootstrap import get_db
from database.schema import CategoryResponse, CategoryRequestBody, category_as_form, CategoryResponseModel, \
    CategoriesResponse

router = APIRouter(tags=["Categories"])

''' CATEGORIES APIs '''
@router.get('/categories', response_model=CategoriesResponse)
async def list_category(search: str | None = Query(None), db: Session = Depends(get_db) ):
    return CategoryController.index(search, db)

@router.get('/categories/{category_id}', response_model=CategoryResponseModel)
async def show_category(category_id, db: Session = Depends(get_db)):
    return CategoryController.show(category_id, db)

@router.post('/categories', response_model=CategoryResponse)
async def create_category(request: CategoryRequestBody = Depends(category_as_form), db: Session = Depends(get_db)):
    return CategoryController.store(request, db)

@router.delete('/categories/{category_id}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryController.destroy(category_id, db)



@router.put('/categories/{category_id}', response_model=CategoryResponse)
async def update_category(category_id: int, category_body: CategoryRequestBody, db: Session = Depends(get_db)):
    return CategoryController.update(category_id, category_body, db)
