import enum
from datetime import datetime
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel
from pydantic.v1 import UUID4

from app.enums import RoleEnum


class RegisterRoles(enum.Enum):
    READER = RoleEnum.READER.name
    AUTHOR = RoleEnum.AUTHOR.name

class RegisterRequestBody(BaseModel):
    f_name: str
    l_name: str
    username: str
    password: str
    role: RegisterRoles

async def register_as_form(
        f_name: str = Form(...),
        l_name: str = Form(...),
        role: RegisterRoles = Form(...),
        username: str = Form(...),
        password: str = Form(...)
) -> RegisterRequestBody:
    return RegisterRequestBody(
        f_name=f_name,
        l_name=l_name,
        role=role,
        username=username,
        password=password
    )




class UserResponseModel(BaseModel):
    id: str
    name: str
    username: str
    role: str

class RegistrationResponseModel(BaseModel):
    success: bool
    message: str
    data: UserResponseModel

class PersonalAccessModel(BaseModel):
    token: str
    expires_at: datetime
    user_id: UUID


class LoginResponseModel(BaseModel):
    success: bool
    message: str
    data: PersonalAccessModel