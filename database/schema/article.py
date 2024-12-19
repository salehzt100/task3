from typing import List
from uuid import UUID

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from . import TagResponseModel
from .user import  UserResponse
from .category import CategoryResponseModel


class ArticleStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"




class ArticleRequestBody(BaseModel):
    title: str
    body: str
    user_id: UUID
    category_id: int
    tags:List[int]

class ArticleResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    status: ArticleStatus
    user: UserResponse
    category: CategoryResponseModel
    tags: List[TagResponseModel]
