from typing import Type

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
    def check_exists(db: Session, name: str) -> bool:
        return db.query(Category).filter_by(name=name).first() is not None

    @staticmethod
    def get_all(db: Session, search: str | None) :
        query = db.query(Category)
        if search:
            query = query.filter(Category.name.ilike(f"%{search}%"))

        return query.all()

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()