from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.repositories import CategoryRepository
from app.services import CategoryServices
from database.schema import CategoryRequestBody, CategoryResponse, CategoryResponseModel, CategoriesResponse
from utils import exception_handler


class CategoryController:

    @staticmethod
    @exception_handler
    def store(request: CategoryRequestBody, db: Session):
        category = CategoryServices.create_new_category(request, db)
        return CategoryResponse(
            success=True,
            message="Category created",
            data=CategoryResponseModel(
                id=category.id,
                name=category.name,

            ),
        )

    @staticmethod
    @exception_handler
    def index(search, db):

        categories = CategoryRepository.get_all(db=db, search=search)

        return CategoriesResponse(
            success=True,
            message="Categories retrieved successfully",
            data=[CategoryResponseModel(**category.__dict__) for category in categories],
        )

    @staticmethod
    @exception_handler
    def show(category_id: int, db: Session):
        category = CategoryRepository.get_by_id(db=db, category_id=category_id)

        if category is None:
            raise NotFoundException("Category not found")
        return CategoryResponseModel(**category)

    @staticmethod
    @exception_handler
    def destroy(category_id: int, db: Session):
        category = CategoryRepository.get_by_id(db=db, category_id=category_id)

        if category is None:
            raise NotFoundException(f"Category with id '{category_id}' not found")

        CategoryRepository.delete_category(db, category)

        return {
            "success": True,
            "message": "Category deleted successfully",
        }


    @staticmethod
    @exception_handler
    def update(category_id: int,request: CategoryRequestBody, db: Session):

        category = CategoryServices.update_category(category_id, request, db)

        return CategoryResponse(
            success=True,
            message="Category updated successfully",
            data=CategoryResponseModel(**category.__dict__),
        )
