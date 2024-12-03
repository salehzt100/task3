from typing import List

from fastapi import APIRouter

from database.schema import CategoryResponse, CategoryRequestBody

router = APIRouter(tags=["Categories"])

''' CATEGORIES APIs '''
@router.get('/categories', response_model=List[CategoryResponse])
async def list_category():
    pass

@router.get('/categories/{category_id}', response_model=CategoryResponse)
async def show_category(category_id: int):
    pass

@router.post('/categories', response_model=CategoryResponse)
async def create_category(category_body: CategoryRequestBody):
    pass

@router.put('/categories/{category_id}', response_model=CategoryResponse)
async def update_category(category_id: int, category_body: CategoryRequestBody):
    pass

@router.delete('/categories/{category_id}', response_model=dict)
async def delete_category(category_id: int):
    pass
