from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from core.config import settings
from core.security import verify_password, create_access_token, hash_password
from database import RegistrationResponseModel
from database.schema import UserResponseModel
from ..exceptions import CustomException
from ..repositories.auth_repository import AuthRepository
from ..models import User, PersonalAccessToken
from ..enums import RoleEnum


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.auth_repository = AuthRepository(db)

    def register_user(self, user_request):
        """
        Handles the user registration process.
        """
        user_exists = self.auth_repository.get_user_by_username(user_request.username)
        if user_exists:
            raise CustomException(f'Username {user_request.username} already exists')

        hashed_password = hash_password(user_request.password)

        new_user = User(
            name=f"{user_request.f_name} {user_request.l_name}",
            username=user_request.username,
            password=hashed_password,
            role_id=RoleEnum[user_request.role.value].value,
            is_active=True if user_request.role.name == RoleEnum.READER.name else False,
        )

        created_user = self.auth_repository.create_user(new_user)

        message = (
            "User created successfully. Please wait for admin approval."
            if user_request.role.name == RoleEnum.AUTHOR.name
            else "User created successfully."
        )

        return RegistrationResponseModel(
            success=True,
            message=message,
            data=UserResponseModel(
                id=created_user.id,
                name=created_user.name,
                username=created_user.username,
                role=created_user.role.name,
            ),
        )

    def login_user(self, username: str, password: str):
        """
        Authenticates a user by username and password.
        """
        user = self.auth_repository.get_user_by_username(username)
        if not user:
            raise CustomException("Invalid username or password", status_code=404)

        if not verify_password(password, str(user.password)):
            raise CustomException("Invalid credentials", status_code=401)

        if not user.is_active:
            raise CustomException("Account is not active", status_code=403)

        access_token = self.auth_repository.get_active_token(user.id)

        if  access_token:
            self.auth_repository.delete_token(access_token)

        new_access_token = create_access_token(sub=user.username)

        new_token = PersonalAccessToken(
            name=f"access_token_for_{user.username}",
            token=new_access_token,
            user_id=user.id,
            expires_at=datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            last_used_at=datetime.now(),
        )

        access_token = self.auth_repository.add_token(new_token)

        return {"access_token": access_token.token, "token_type": "bearer"}
