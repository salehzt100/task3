from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers import UserController
from database import UserResponseModel
from database.schema import (
    UserResponse,
    user_post_as_form,
    UpdateUserRequestBody,
    user_put_as_form, AddUserRequestBody,
)
from utils.fastapi.dependencies import role_required

router = APIRouter(tags=["Users"])

''' USER APIs '''

@router.get(
    '/users/active',
    response_model=List[UserResponse],
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def list_active_users(user_controller: UserController = Depends(UserController)):
    return user_controller.all_active_users()


@router.get(
    '/users/inactive',
    response_model=List[UserResponse],
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def list_inactive_users(user_controller: UserController = Depends(UserController)):
    return user_controller.all_inactive_users()


@router.get(
    '/users/inactive/authors',
    response_model=List[UserResponse],
    dependencies=[Depends(role_required(['ADMIN']))],
)
async def all_inactive_authors(user_controller: UserController = Depends(UserController)):
    return user_controller.all_inactive_authors()


@router.get(
    '/users/{user_id}',
    response_model=UserResponseModel,
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def show_user(user_id: UUID, user_controller: UserController = Depends(UserController)):
    return user_controller.get_user_py_id(user_id)


@router.post(
    '/users',
    response_model=UserResponse,
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def create_user(
    user_body: AddUserRequestBody = Depends(user_post_as_form),
    user_controller: UserController = Depends(UserController)
):
    return user_controller.stor(user_body)


@router.put(
    '/users/{user_id}',
    response_model=UserResponseModel,
    dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))]
)
async def update_user(
    user_id: UUID,
    user_request: UpdateUserRequestBody = Depends(user_put_as_form),
    user_controller: UserController = Depends(UserController)
):
    return user_controller.update(user_id, user_request)


@router.delete(
    '/users/{user_id}',
    response_model=dict,
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def delete_user(user_id: UUID, user_controller: UserController = Depends(UserController)):
    return user_controller.destroy(user_id)


@router.patch(
    '/users/{user_id}/activate',
    response_model=dict,
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def activate_user(user_id: UUID, user_controller: UserController = Depends(UserController)):
    return user_controller.activate_users(user_id)


@router.patch(
    '/users/{user_id}/inactivate',
    response_model=dict,
    dependencies=[Depends(role_required(['ADMIN']))]
)
async def inactivate_user(user_id: UUID, user_controller: UserController = Depends(UserController)):
    return user_controller.inactivate_users(user_id)
