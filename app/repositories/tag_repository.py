from sqlalchemy.orm import Session
from app.models import Tag

class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, tag: Tag) -> Tag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def check_exists(self, name: str, exclude_id: int | None = None) -> bool:
        query = self.db.query(Tag).filter(Tag.name == name)
        if exclude_id is not None:
            query = query.filter(Tag.id != exclude_id)  # Exclude the current tag ID
        return query.first() is not None

    def check_exists_by_id(self, tag_id: int) -> bool:
        query = self.db.query(Tag).filter(Tag.id == tag_id)
        return query.first() is not None

    def get_all(self, search: str | None = None):
        query = self.db.query(Tag)
        if search:
            query = query.filter(Tag.name.ilike(f"%{search}%"))
        return query.all()

    def get_by_id(self, tag_id: int):
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def delete_tag(self, tag: Tag):
        self.db.delete(tag)
        self.db.commit()

    def update_tag(self, tag_id: int, name: str):
        updated_tag = self.db.query(Tag).filter(Tag.id == tag_id).update({Tag.name: name})
        self.db.commit()
        return updated_tag
