
from sqlalchemy.orm import Session
from app.models import Tag


class TagRepository:

    @staticmethod
    def create_tag(db: Session, tag: Tag) -> Tag:
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def check_exists(db: Session, name: str, exclude_id: int | None = None) -> bool:
        query = db.query(Tag).filter(Tag.name == name)
        if exclude_id is not None:
            query = query.filter(Tag.id != exclude_id)  # Exclude the current tag ID
        return query.first() is not None

    @staticmethod
    def check_exists_py_id(db: Session, tag_id: int) -> bool:
        query = db.query(Tag).filter(Tag.id == tag_id)
        return query.first() is not None

    @staticmethod
    def get_all(db: Session, search: str | None):
        query = db.query(Tag)
        if search:
            query = query.filter(Tag.name.ilike(f"%{search}%"))
        return query.all()

    @staticmethod
    def get_by_id(db: Session, tag_id: int):
        return db.query(Tag).filter(Tag.id == tag_id).first()

    @staticmethod
    def delete_tag(db: Session, tag: Tag):
        db.delete(tag)
        db.commit()

    @staticmethod
    def update_tag(db: Session, tag_id: int, name: str):
        updated_tag = db.query(Tag).filter(Tag.id == tag_id).update({Tag.name: name})
        db.commit()
        return updated_tag
