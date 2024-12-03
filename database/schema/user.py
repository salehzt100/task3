from pydantic import BaseModel
from datetime import datetime

class UserRequestBody(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role_id: int

class UserResponse(BaseModel):
    id: int
    full_name: str
    role: str
    created_at: datetime
