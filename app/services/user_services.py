from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException, ValidationException
from app.models import User
from app.repositories.user_repository import UserRepository
from core.security import hash_password
from database.schema import UpdateUserRequestBody, AddUserRequestBody


class UserServices:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def activate_user(self, user_id: UUID):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(f'User with id {user_id} not found')

        return self.user_repository.activate_user(user)

    def inactivate_user(self, user_id: UUID):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(f'User with id {user_id} not found')

        return self.user_repository.inactivate_user(user)

    def create_user(self, user_request: AddUserRequestBody):

        # Hash the password
        hashed_password = hash_password(user_request.password)

        # Create user instance
        new_user = User(
            name=f"{user_request.f_name} {user_request.l_name}",
            username=user_request.username,
            password=hashed_password,
            role_id=user_request.role.value,
            is_active=True,
        )

        # Save user using the repository
        created_user = self.user_repository.create_user(new_user)
        return created_user

    def update_user(self, user_id, user_request: UpdateUserRequestBody):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(F'user with id {user_id} not found')
        if self.user_repository.check_duplicate_username(user_id, user_request.username):
            raise ValidationException(f'username {user_request.username} already exists')

        data_to_update = {key: value for key, value in dict(user_request).items() if value is not None}

        for key, value in data_to_update.items():
            setattr(user, key, value)

        self.user_repository.update_user(user)

        return user
