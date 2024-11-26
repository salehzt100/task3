import enum
from pydantic import BaseModel
from Enums import RoleEnum

class RegisterRoles(enum.Enum):
    READER = RoleEnum.READER.value
    AUTHOR = RoleEnum.AUTHOR.value

class RegisterRequestBody(BaseModel):
    username: str
    password: str
    name: str
    role_id: RegisterRoles

class LoginRequestBody(BaseModel):
    username: str
    password: str
