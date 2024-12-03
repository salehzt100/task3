from pydantic import BaseModel

class TagRequestBody(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: int
    name: str
