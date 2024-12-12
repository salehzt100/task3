
from sqlalchemy.orm import Session

from app.exceptions import ValidationException
from app.models import Category
from app.repositories import CategoryRepository
from database.schema import CategoryRequestBody


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

    @staticmethod
    def update_category(category_id: int,request: CategoryRequestBody, db: Session):
        category = CategoryRepository.get_by_id(db, category_id)
        if category is None:
            raise ValidationException(f"Category with id: {category_id} does not exist")

        if request.name.isdigit():
            raise ValidationException("Category name cannot be an integer")
        if CategoryRepository.check_exists(db, request.name, category_id):
            raise ValidationException(f"Category with name: '{request.name}' already exists")

        CategoryRepository.update_category(db, category_id, request.name)
        updated_category = CategoryRepository.get_by_id(db, category_id)
        return updated_category


