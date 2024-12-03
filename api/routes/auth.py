from contextvars import Token
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.controllers import AuthController
from bootstrap import get_db
from database import  register_as_form
from database.schema import RegisterRequestBody, RegistrationResponseModel
from fastapi.security import  OAuth2PasswordRequestForm

router = APIRouter(tags=["Auth"])

''' AUTH APIs '''
@router.post("/register",response_model=RegistrationResponseModel)
async def register( user: RegisterRequestBody = Depends(register_as_form), db: Session = Depends(get_db)):
    return AuthController.register(user, db)

@router.post("/login")
async def login(request: Annotated[OAuth2PasswordRequestForm,Depends()] ,db: Session = Depends(get_db)):
    return AuthController.login(request.username,request.password, db)

@router.post("/logout")
async def logout():
    pass


