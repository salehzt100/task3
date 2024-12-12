from datetime import datetime

from pydantic import BaseModel
from typing import List
from fastapi import Form

class TagRequestBody(BaseModel):
    name: str

class TagResponseModel(BaseModel):
    id: int
    name: str
    created_at: datetime



class TagResponse(BaseModel):
    success: bool
    message: str
    data: TagResponseModel

class TagsResponse(BaseModel):
    success: bool
    message: str
    data: List[TagResponseModel]



def tag_as_form(
        name: str =Form(...),
)->TagRequestBody:
    return TagRequestBody(
        name=name,
    )