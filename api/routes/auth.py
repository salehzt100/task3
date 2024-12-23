from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers import AuthController
from database.schema import RegisterRequestBody, RegistrationResponseModel
from database import register_as_form

router = APIRouter(tags=["Auth"])

''' AUTH APIs '''

@router.post(
    "/register",
    response_model=RegistrationResponseModel,
    summary="Register a new user."
)
async def register(
    user: RegisterRequestBody = Depends(register_as_form),
    auth_controller: AuthController = Depends(AuthController)
):
    """
    Registers a new user with the provided details.
    """
    return auth_controller.register(user)

@router.post(
    "/login",
    response_model=dict,
    summary="Login with username and password."
)
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_controller: AuthController = Depends(AuthController)
):
    """
    Authenticates a user and returns a token for accessing protected routes.
    """
    return auth_controller.login(request.username, request.password)
