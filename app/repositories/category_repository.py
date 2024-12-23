from sqlalchemy.orm import Session
from app.models import Category

class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def check_exists(self, name: str, exclude_id: int | None = None) -> bool:
        query = self.db.query(Category).filter(Category.name == name)
        if exclude_id is not None:
            query = query.filter(Category.id != exclude_id)  # Exclude the current category ID
        return query.first() is not None

    def check_exists_py_id(self, category_id: int) -> bool:
        query = self.db.query(Category).filter(Category.id == category_id)
        return query.first() is not None

    def get_all(self, search: str | None):
        query = self.db.query(Category)
        if search:
            query = query.filter(Category.name.ilike(f"%{search}%"))
        return query.all()

    def get_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()

    def delete_category(self, category: Category):
        self.db.delete(category)
        self.db.commit()

    def update_category(self, category_id: int, name: str):
        updated_category = self.db.query(Category).filter(Category.id == category_id).update({Category.name: name})
        self.db.commit()
        return updated_category
