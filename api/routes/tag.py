from fastapi import APIRouter, Depends, Query
from app.controllers.tag_controller import TagController
from database.schema import (
    TagResponse,
    TagRequestBody,
    tag_as_form,
    TagResponseModel,
    TagsResponse
)
from utils.fastapi.dependencies import role_required

# Initialize router
router = APIRouter(
    tags=["Tags"],
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)

''' TAGS APIs '''

@router.get(
    '/tags',
    response_model=TagsResponse,
    summary="List all tags with optional search",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def list_tag(
    search: str | None = Query(None, description="Search term to filter tags."),
    tag_controller: TagController = Depends(TagController)
):
    return tag_controller.index(search)


@router.get(
    '/tags/{tag_id}',
    response_model=TagResponseModel,
    summary="Get details of a specific tag",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def show_tag(
    tag_id: int,
    tag_controller: TagController = Depends(TagController)
):
    return tag_controller.show(tag_id)


@router.post(
    '/tags',
    response_model=TagResponse,
    summary="Create a new tag",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def create_tag(
    request: TagRequestBody = Depends(tag_as_form),
    tag_controller: TagController = Depends(TagController)
):
    return tag_controller.store(request)


@router.delete(
    '/tags/{tag_id}',
    response_model=dict,
    summary="Delete a tag by ID",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def delete_tag(
    tag_id: int,
    tag_controller: TagController = Depends(TagController)
):
    return tag_controller.destroy(tag_id)


@router.put(
    '/tags/{tag_id}',
    response_model=TagResponse,
    summary="Update details of a tag",
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def update_tag(
    tag_id: int,
    tag_body: TagRequestBody,
    tag_controller: TagController = Depends(TagController)
):
    return tag_controller.update(tag_id, tag_body)
