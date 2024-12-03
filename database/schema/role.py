from pydantic import BaseModel

class RoleRequestBody(BaseModel):
    name: str

class RoleResponse(BaseModel):
    id: int
    name: str
