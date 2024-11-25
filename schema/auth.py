from pydantic import BaseModel

class RegisterRequestBody(BaseModel):
    username: str
    password: str
    name: str
    role_id: int

class LoginRequestBody(BaseModel):
    username: str
    password: str
