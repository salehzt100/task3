from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends


from app.controllers import UserController
from bootstrap import get_db
from database import UserResponseModel
from utils import oauth2_scheme
from sqlalchemy.orm import Session

from database.schema import UserResponse, UserRequestBody, user_post_as_form, UpdateUserRequestBody, user_put_as_form

router = APIRouter(tags=["Users"])

''' USER APIs '''
@router.get('/users/active', response_model=List[UserResponse])
async def list_active_users(db: Session  = Depends(get_db)):
    return UserController.all_active_users(db)
@router.get('/users/inactive', response_model=List[UserResponse])
async def list_inactive_users(db: Session  = Depends(get_db)):
    return UserController.all_inactive_users(db)
@router.get('/users/inactive/authors', response_model=List[UserResponse])
async def all_inactive_authors(db: Session  = Depends(get_db)):
    return UserController.all_inactive_authors(db)


@router.get('/users/{user_id}', response_model=UserResponseModel)
async def show_user(user_id: UUID, db: Session  = Depends(get_db)):
    return UserController.get_user_py_id(db, user_id)

@router.post('/users', response_model=UserResponse)
async def create_user(user_body: UserRequestBody = Depends(user_post_as_form),  db: Session  = Depends(get_db)):
    return UserController.stor(db, user_body)

@router.put('/users/{user_id}', response_model=UserResponseModel)
async def update_user(user_id: UUID, user_request: UpdateUserRequestBody = Depends(user_put_as_form), db: Session = Depends(get_db)):
    return UserController.update(db, user_id, user_request)

@router.delete('/users/{user_id}')
async def delete_user(user_id: UUID, db: Session  = Depends(get_db)):
    return UserController.destroy(db, user_id)
