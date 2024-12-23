from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.controllers.category_controller import CategoryController
from database.schema import CategoryResponse, CategoryRequestBody, category_as_form, CategoryResponseModel, CategoriesResponse
from utils.fastapi.dependencies import role_required

router = APIRouter(
    tags=["Categories"],
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)

''' CATEGORIES APIs '''

@router.get(
    '/categories',
    response_model=CategoriesResponse,
    summary="Retrieve a list of categories, optionally filtered by a search term.",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def list_category(
    search: str | None = Query(None, description="Search term to filter categories."),
    category_controller: CategoryController = Depends(CategoryController)
):
    return category_controller.index(search)

@router.get(
    '/categories/{category_id}',
    response_model=CategoryResponseModel,
    summary="Retrieve details of a specific category by its ID.",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def show_category(
    category_id: int,
    category_controller: CategoryController = Depends(CategoryController)
):
    return category_controller.show(category_id)

@router.post(
    '/categories',
    response_model=CategoryResponse,
    summary="Create a new category with the provided details.",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def create_category(
    request: CategoryRequestBody = Depends(category_as_form),
    category_controller: CategoryController = Depends(CategoryController)
):
    return category_controller.store(request)

@router.delete(
    '/categories/{category_id}',
    response_model=dict,
    summary="Delete a specific category by its ID.",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def delete_category(
    category_id: int,
    category_controller: CategoryController = Depends(CategoryController)
):
    return category_controller.destroy(category_id)

@router.put(
    '/categories/{category_id}',
    response_model=CategoryResponse,
    summary="Update an existing category's details by its ID.",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def update_category(
    category_id: int,
    category_body: CategoryRequestBody,
    category_controller: CategoryController = Depends(CategoryController)
):
    return category_controller.update(category_id, category_body)
