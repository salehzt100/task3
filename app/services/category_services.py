
from sqlalchemy.orm import Session

from app.exceptions import ValidationException
from app.models import Category
from app.repositories.category_repository import CategoryRepository
from database.schema import CategoryRequestBody, CategoryResponseModel, CategoryResponse
from utils import exception_handler


class CategoryServices:

    @staticmethod
    def create_new_category(request: CategoryRequestBody, db: Session):

        if request.name.isdigit():
            raise ValidationException("Category name cannot be an integer")
        if  CategoryRepository.check_exists(db, request.name):
            raise ValidationException(f"Category with name: '{request.name}' already exists")

        category_data = Category(name=request.name)
        new_category = CategoryRepository.create_category(db, category_data)
        return new_category


