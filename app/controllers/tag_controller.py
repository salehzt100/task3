from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.repositories import TagRepository
from app.services import TagServices
from bootstrap import get_db
from database.schema import TagRequestBody, TagResponse, TagResponseModel, TagsResponse
from utils import exception_handler


class TagController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.tag_services = TagServices(db)
        self.tag_repository = TagRepository(db)

    @exception_handler
    def store(self, request: TagRequestBody):
        """
        Create a new tag.
        """
        tag = self.tag_services.create_new_tag(request)
        return TagResponse(
            success=True,
            message="Tag created",
            data=TagResponseModel(
                id=tag.id,
                name=tag.name,
                created_at=tag.created_at,
            ),
        )

    @exception_handler
    def index(self, search: str = ""):
        """
        Retrieve all tags, optionally filtered by search.
        """
        tags = self.tag_repository.get_all(search)
        return TagsResponse(
            success=True,
            message="Tags retrieved successfully",
            data=[TagResponseModel(**tag.__dict__) for tag in tags],
        )

    @exception_handler
    def show(self, tag_id: int):
        """
        Retrieve a tag by its ID.
        """
        tag = self.tag_repository.get_by_id(tag_id)
        if tag is None:
            raise NotFoundException(f"Tag with id '{tag_id}' not found")
        return TagResponseModel(**tag.__dict__)

    @exception_handler
    def destroy(self, tag_id: int):
        """
        Delete a tag by its ID.
        """
        tag = self.tag_repository.get_by_id(tag_id)
        if tag is None:
            raise NotFoundException(f"Tag with id '{tag_id}' not found")
        self.tag_repository.delete_tag(tag)
        return {
            "success": True,
            "message": "Tag deleted successfully",
        }

    @exception_handler
    def update(self, tag_id: int, request: TagRequestBody):
        """
        Update a tag by its ID.
        """
        tag = self.tag_services.update_tag(tag_id, request)
        return TagResponse(
            success=True,
            message="Tag updated successfully",
            data=TagResponseModel(**tag.__dict__),
        )
