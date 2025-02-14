from datetime import datetime
from typing import List, Type

from fastapi import Form
from pydantic import BaseModel


class CategoryRequestBody(BaseModel):
    name: str

class CategoryResponseModel(BaseModel):
    id: int
    name: str
    created_at: datetime

class CategoryResponse(BaseModel):
    success: bool
    message: str
    data: CategoryResponseModel

class CategoriesResponse(BaseModel):
    success: bool
    message: str
    data: List[CategoryResponseModel]




def category_as_form(
        name: str =Form(...),
)->CategoryRequestBody:
    return CategoryRequestBody(
        name=name,
    )