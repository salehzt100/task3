from sqlalchemy.orm import Session
from app.exceptions import ValidationException
from app.models import Tag
from app.repositories import TagRepository
from database.schema import TagRequestBody


class TagServices:
    def __init__(self, db: Session):
        self.tag_repository = TagRepository(db)
        self.db = db

    def create_new_tag(self, request: TagRequestBody):
        if request.name.isdigit():
            raise ValidationException("Tag name cannot be an integer")
        if self.tag_repository.check_exists(request.name):
            raise ValidationException(f"Tag with name: '{request.name}' already exists")

        tag_data = Tag(name=request.name)
        new_tag = self.tag_repository.create_tag(tag_data)
        return new_tag

    def update_tag(self, tag_id: int, request: TagRequestBody):
        tag = self.tag_repository.get_by_id(tag_id)
        if tag is None:
            raise ValidationException(f"Tag with id: {tag_id} does not exist")

        if request.name.isdigit():
            raise ValidationException("Tag name cannot be an integer")
        if self.tag_repository.check_exists(request.name, tag_id):
            raise ValidationException(f"Tag with name: '{request.name}' already exists")

        self.tag_repository.update_tag(tag_id, request.name)
        updated_tag = self.tag_repository.get_by_id(tag_id)
        return updated_tag
