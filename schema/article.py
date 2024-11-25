from pydantic import BaseModel
from datetime import datetime
from typing import List
from enum import Enum
from .user import UserResponse
from .category import CategoryResponse

class ArticleStatus(str, Enum):
    draft = "draft"
    in_review = "in_review"
    published = "published"
    rejected = "rejected"

class ArticleRequestBody(BaseModel):
    title: str
    body: str
    user_id: int
    status: ArticleStatus
    category_id: int

class ArticleResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    status: ArticleStatus
    user: UserResponse
    category: CategoryResponse
