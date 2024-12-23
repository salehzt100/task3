from fastapi import Depends
from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.repositories import CategoryRepository
from app.services import CategoryServices
from bootstrap import get_db
from database.schema import (
    CategoryRequestBody,
    CategoryResponse,
    CategoryResponseModel,
    CategoriesResponse
)
from utils import exception_handler


class CategoryController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.category_services = CategoryServices(db)
        self.category_repository = CategoryRepository(db)

    @exception_handler
    def store(self, request: CategoryRequestBody):
        """
        Create a new category.
        """
        category = self.category_services.create_new_category(request)
        return CategoryResponse(
            success=True,
            message="Category created",
            data=CategoryResponseModel(
                id=category.id,
                name=category.name,
                created_at=category.created_at,
            ),
        )

    @exception_handler
    def index(self, search: str = ""):
        """
        Retrieve all categories, optionally filtered by search.
        """
        categories = self.category_repository.get_all(search)
        return CategoriesResponse(
            success=True,
            message="Categories retrieved successfully",
            data=[CategoryResponseModel(**category.__dict__) for category in categories],
        )

    @exception_handler
    def show(self, category_id: int):
        """
        Retrieve a category by its ID.
        """
        category = self.category_repository.get_by_id(category_id)
        if category is None:
            raise NotFoundException("Category not found")
        return CategoryResponseModel(**category.__dict__)

    @exception_handler
    def destroy(self, category_id: int):
        """
        Delete a category by its ID.
        """
        category = self.category_repository.get_by_id(category_id)
        if category is None:
            raise NotFoundException(f"Category with id '{category_id}' not found")
        self.category_repository.delete_category(category)
        return {
            "success": True,
            "message": "Category deleted successfully",
        }

    @exception_handler
    def update(self, category_id: int, request: CategoryRequestBody):
        """
        Update a category by its ID.
        """
        category = self.category_services.update_category(category_id, request)
        return CategoryResponse(
            success=True,
            message="Category updated successfully",
            data=CategoryResponseModel(**category.__dict__),
        )
