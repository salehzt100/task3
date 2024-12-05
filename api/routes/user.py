from typing import List

from fastapi import APIRouter, Depends

from app.controllers import UserController
from utils import oauth2_scheme

from database.schema import UserResponse, UserRequestBody

router = APIRouter(tags=["Users"])

''' USER APIs '''
@router.get('/users/{user_id}/active', response_model=List[UserResponse])
async def list_active_users(token: str = Depends(oauth2_scheme)):
    pass
@router.post('/users/{user_id}/inactive', response_model=List[UserResponse])
async def list_inactive_users(token: str = Depends(oauth2_scheme)):
    pass

@router.post('/users/active', response_model=List[UserResponse])
async def active_user(token: str = Depends(oauth2_scheme)):
    pass
@router.get('/users/inactive', response_model=List[UserResponse])
async def inactive_user(token: str = Depends(oauth2_scheme)):
    pass

@router.get('/users/{user_id}', response_model=UserResponse)
async def show_user(user_id: int):
    pass

@router.post('/users', response_model=UserResponse)
async def create_user(user_body: UserRequestBody):
    pass

@router.put('/users/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, user_body: UserRequestBody):
    pass

@router.delete('/users/{user_id}', response_model=dict)
async def delete_user(user_id: int):
    pass
