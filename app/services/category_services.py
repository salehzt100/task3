from sqlalchemy.orm import Session
from app.exceptions import ValidationException
from app.models import Category
from app.repositories import CategoryRepository
from database.schema import CategoryRequestBody


class CategoryServices:

    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def create_new_category(self, request: CategoryRequestBody):
        # Check if the category name is a number
        if request.name.isdigit():
            raise ValidationException("Category name cannot be an integer")
        # Check if a category with the same name already exists
        if self.category_repository.check_exists(request.name):
            raise ValidationException(f"Category with name: '{request.name}' already exists")

        # Create the new category
        category_data = Category(name=request.name)
        new_category = self.category_repository.create_category(category_data)

        return new_category

    def update_category(self, category_id: int, request: CategoryRequestBody):
        # Check if the category exists
        category = self.category_repository.get_by_id(category_id)
        if category is None:
            raise ValidationException(f"Category with id: {category_id} does not exist")

        # Check if the category name is a number
        if request.name.isdigit():
            raise ValidationException("Category name cannot be an integer")
        # Check if a category with the same name already exists
        if self.category_repository.check_exists(request.name, category_id):
            raise ValidationException(f"Category with name: '{request.name}' already exists")

        # Update the category name
        self.category_repository.update_category(category_id, request.name)
        updated_category = self.category_repository.get_by_id(category_id)

        return updated_category
