import enum
from typing import Optional
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel

from app.enums import RoleEnum


class UserRequestBody(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role_id: int



class UserResponseModel(BaseModel):
    id: UUID
    username: str
    name: str
    role: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    role: str


class PostUserRoles(enum.IntEnum):
    READER = RoleEnum.READER.value
    AUTHOR = RoleEnum.AUTHOR.value
    EDITOR = RoleEnum.EDITOR.value
    ADMIN = RoleEnum.ADMIN.value

class AddUserRequestBody(BaseModel):
    f_name: str
    l_name: str
    username: str
    password: str
    role: PostUserRoles



async def user_post_as_form(
        f_name: str = Form(...),
        l_name: str = Form(...),
        role: PostUserRoles = Form(...),
        username: str = Form(...),
        password: str = Form(...)
) -> AddUserRequestBody:
    return AddUserRequestBody(
        f_name=f_name,
        l_name=l_name,
        role=role,
        username=username,
        password=password
    )


class UpdateUserRequestBody(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    role_id: Optional[int] = None
async def user_put_as_form(
        name: Optional[str] = Form(None),
        role_id: Optional[int] = Form(None),
        username: Optional[str] = Form(None),
) -> UpdateUserRequestBody:
    return UpdateUserRequestBody(
        name=name,
        role_id=role_id,
        username=username,
    )






