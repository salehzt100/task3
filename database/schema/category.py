from pydantic import BaseModel

class CategoryRequestBody(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
