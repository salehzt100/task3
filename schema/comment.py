from pydantic import BaseModel
from datetime import datetime
from .user import UserResponse

class CommentRequestBody(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    user: UserResponse
    article_id: int
    created_at: datetime
