from sqlalchemy.orm import Session
from app.exceptions import ValidationException
from app.models import Tag
from app.repositories import TagRepository
from database.schema import TagRequestBody


class TagServices:

    @staticmethod
    def create_new_tag(request: TagRequestBody, db: Session):
        if request.name.isdigit():
            raise ValidationException("Tag name cannot be an integer")
        if TagRepository.check_exists(db, request.name):
            raise ValidationException(f"Tag with name: '{request.name}' already exists")

        tag_data = Tag(name=request.name)
        new_tag = TagRepository.create_tag(db, tag_data)
        return new_tag

    @staticmethod
    def update_tag(tag_id: int, request: TagRequestBody, db: Session):
        tag = TagRepository.get_by_id(db, tag_id)
        if tag is None:
            raise ValidationException(f"Tag with id: {tag_id} does not exist")

        if request.name.isdigit():
            raise ValidationException("Tag name cannot be an integer")
        if TagRepository.check_exists(db, request.name, tag_id):
            raise ValidationException(f"Tag with name: '{request.name}' already exists")

        TagRepository.update_tag(db, tag_id, request.name)
        updated_tag = TagRepository.get_by_id(db, tag_id)
        return updated_tag
