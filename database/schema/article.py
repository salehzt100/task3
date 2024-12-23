from typing import List, Optional
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from .user import  UserResponse
from .category import CategoryResponseModel
from .comment import CommentResponseModel
from .tag import TagResponseModel


class ArticleStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"

class ArticleFilterType(str, Enum):
    DATE = 'date'
    STATUS = 'status'
    AUTHOR = 'author'







class ArticleRequestBody(BaseModel):
    title: str
    body: str
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
    comments: List[CommentResponseModel]



class ArticleUpdateRequestBody(BaseModel):
    title: Optional[str] = Form(None),
    body: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    tags: Optional[List[int]] = Form(None),


