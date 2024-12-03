from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from core.config import settings
from core.security import verify_password, create_access_token, hash_password
from database import RegistrationResponseModel
from database.schema import UserResponseModel
from utils import  exception_handler
from ..exceptions import CustomException
from ..repositories.auth_repository import AuthRepository
from ..models import User, PersonalAccessToken
from ..enums import RoleEnum


class AuthService:

    @staticmethod
    @exception_handler

    def register_user(user_request, db: Session):
        """
        Handles the user registration process.
        """
        # Hash the password
        hashed_password = hash_password(user_request.password)

        # Create user instance
        new_user = User(
            name=f"{user_request.f_name} {user_request.l_name}",
            username=user_request.username,
            password=hashed_password,
            role_id=RoleEnum[user_request.role.value].value,
            is_active=True if user_request.role.name == RoleEnum.READER.name else False,
        )

        # Save user using the repository
        created_user = AuthRepository.create_user(db, new_user)


        message = (
            "User created successfully. Please wait for admin approval."
            if user_request.role.name == RoleEnum.AUTHOR.name
            else "User created successfully."
        )

        return RegistrationResponseModel(
            success=True,
            message=message,
            data=UserResponseModel(
                id=str(created_user.id),
                name=created_user.name,
                username=created_user.username,
                role=str(created_user.role.name),
            ),
        )





    @staticmethod
    @exception_handler
    def login_user(username,password , db: Session):
        """
        Authenticates a user by username and password.
        """

        user = AuthRepository.get_user_by_username(db, username)

        if not user:
            raise CustomException("Invalid username or password",status_code=404)

        if not verify_password(password, str(user.password)):
            raise CustomException("Invalid Credentials",status_code=401)

        if not user.is_active:
            raise CustomException("Account is not active",status_code=403)

        access_token = AuthRepository.get_active_token(db, user.id)
        if not access_token:
            # generate jwt token
            new_access_token = create_access_token(sub=user.username)

            new_token = PersonalAccessToken(
                name=f"access_token_for_{user.username}",
                token=new_access_token,
                user_id=user.id,
                expires_at= datetime.now() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                last_used_at=datetime.now(),
            )

            access_token = AuthRepository.add_token(db, new_token)

            return {"access_token": access_token, "token_type": "bearer"}








