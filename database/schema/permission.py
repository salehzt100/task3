from pydantic import BaseModel
from typing import List

class PermissionResponse(BaseModel):
    id: int
    name: str

class RolePermissionRequestBody(BaseModel):
    role_id: int
    permissions: List[int]
