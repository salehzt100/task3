from typing import List, Annotated

import jwt
from fastapi import Depends, HTTPException, Request
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from bootstrap import get_db
from core import security
from core.config import settings


def get_current_user( request: Request, db: Session = Depends(get_db)):
    from app.controllers.auth_controller import AuthController
    auth_controller = AuthController(db)
    token = request.headers.get("Authorization")
    token = token.replace("Bearer ", "")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = auth_controller.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    request.state.user = user
    return user


def role_required(roles: List[str]):

    def role_checker(user  = Depends(get_current_user),):
        print('user', not any(role in [user.role.name] for role in roles))

        for role in roles:
            print('role', role)
        print('role', user.role.name.copy())
        if not any(role in [user.role.name] for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )

    return role_checker

