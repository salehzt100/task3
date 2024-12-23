from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from . import UserResponse

class CommentRequestBody(BaseModel):
    content: str

class CommentUpdateRequestBody(BaseModel):
    content: str



class CommentResponse(BaseModel):
    id: int
    content: str
    user: UserResponse
    article_id: int
    created_at: datetime
class CommentResponseModel(BaseModel):
    id: int
    content: str
    user: UserResponse
    created_at: datetime