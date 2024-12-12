from uuid import UUID

from sqlalchemy.orm import Session

from app.enums import RoleEnum
from app.exceptions import NotFoundException, ValidationException
from app.models import User
from app.repositories.user_repository import UserRepository
from core.security import hash_password
from database.schema import UserRequestBody, UpdateUserRequestBody


class UserServices:
    @staticmethod
    def activate_user(db, user_id: UUID):
     return UserRepository.activate_user(db, user_id)
    @staticmethod
    def create_user(db: Session   , user_request: UserRequestBody):
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
            is_active=True,
        )

        # Save user using the repository
        created_user = UserRepository.create_user(db, new_user)
        return created_user


    @staticmethod
    def update_user(db: Session, user_id,  user_request: UpdateUserRequestBody):
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException(F'user with id {user_id} not found')
        if UserRepository.check_duplicate_username(db, user_id, user_request.username):
            raise ValidationException(F'username exists')
        if user_request.role_id not in RoleEnum._value2member_map_:
            raise ValidationException(F'role id {user_request.role_id} not valid')

        data_to_update = {key: value for key, value in dict(user_request).items() if value is not None}

        for key, value in data_to_update.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user



