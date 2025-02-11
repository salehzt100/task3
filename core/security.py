from datetime import datetime, timedelta, timezone
from typing import Any, Union
from fastapi import HTTPException, Depends
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from bootstrap import get_db
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"





def create_access_token(
        sub: Union[str, Any],
        expires_delta: timedelta = None
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




def hash_password(password: str) -> str:
    """
    Hashes the given password using bcrypt (via CryptContext).
    """
    return pwd_context.hash(password)

def verify_access_token(request, db: Session = Depends(get_db)):
    from app.controllers import AuthController
    auth_controller = AuthController(db)


    token = request.headers.get("Authorization")
    print('token', token)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token is missing. Please provide a valid token.")
    token = token.replace("Bearer ", "")
    print('token without bearer ', token)
    token_in_db = auth_controller.get_personal_access_token(token)
    print('token in databse' , token_in_db.__doc__)


    if token_in_db is None:
        raise HTTPException(detail='token is invalid', status_code=status.HTTP_401_UNAUTHORIZED)
    return token_in_db





