from sqlalchemy.orm import Session
from app.exceptions import NotFoundException
from app.repositories import TagRepository
from app.services import TagServices
from database.schema import TagRequestBody, TagResponse, TagResponseModel, TagsResponse
from utils import exception_handler


class TagController:

    @staticmethod
    @exception_handler
    def store(request: TagRequestBody, db: Session):
        tag = TagServices.create_new_tag(request, db)
        return TagResponse(
            success=True,
            message="Tag created",
            data=TagResponseModel(
                id=tag.id,
                name=tag.name,
            ),
        )

    @staticmethod
    @exception_handler
    def index(search, db):
        tags = TagRepository.get_all(db=db, search=search)
        return TagsResponse(
            success=True,
            message="Tags retrieved successfully",
            data=[TagResponseModel(**tag.__dict__) for tag in tags],
        )

    @staticmethod
    @exception_handler
    def show(tag_id: int, db: Session):
        tag = TagRepository.get_by_id(db=db, tag_id=tag_id)
        if tag is None:
            raise NotFoundException(f"Tag with id '{tag_id}' not found")

        return TagResponseModel(**tag.__dict__)

    @staticmethod
    @exception_handler
    def destroy(tag_id: int, db: Session):
        tag = TagRepository.get_by_id(db=db, tag_id=tag_id)
        if tag is None:
            raise NotFoundException(f"Tag with id '{tag_id}' not found")

        TagRepository.delete_tag(db, tag)
        return {
            "success": True,
            "message": "Tag deleted successfully",
        }

    @staticmethod
    @exception_handler
    def update(tag_id: int, request: TagRequestBody, db: Session):
        tag = TagServices.update_tag(tag_id, request, db)
        return TagResponse(
            success=True,
            message="Tag updated successfully",
            data=TagResponseModel(**tag.__dict__),
        )
