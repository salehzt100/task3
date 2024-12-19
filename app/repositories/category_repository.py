
from sqlalchemy.orm import Session

from app.models import Category




class CategoryRepository:

    @staticmethod
    def create_category(db: Session, category: Category) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category


    @staticmethod
    def check_exists(db: Session, name: str, exclude_id: int | None = None) -> bool:
        query = db.query(Category).filter(Category.name == name)
        if exclude_id is not None:
            query = query.filter(Category.id != exclude_id)  # Exclude the current category ID
        return query.first() is not None

    @staticmethod
    def check_exists_py_id(db: Session, category_id: int) -> bool:
        query = db.query(Category).filter(Category.id == category_id)
        return query.first() is not None

    @staticmethod
    def get_all(db: Session, search: str | None):
        query = db.query(Category)
        if search:
            query = query.filter(Category.name.ilike(f"%{search}%"))

        return query.all()

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def delete_category(db: Session, category: Category):
        db.delete(category)
        db.commit()

    @staticmethod
    def update_category(db: Session, category_id: int, name: str):
        updated_category = db.query(Category).filter(Category.id == category_id).update({Category.name: name})
        db.commit()
        return updated_category
