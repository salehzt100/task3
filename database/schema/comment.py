from pydantic import BaseModel
from datetime import datetime
from .user import UserResponseModel

class CommentRequestBody(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    user: UserResponseModel
    article_id: int
    created_at: datetime
