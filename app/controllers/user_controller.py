from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.repositories.user_repository import UserRepository
from app.services.user_services import UserServices
from database import UserResponseModel
from database.schema import UserResponse, UserRequestBody, UpdateUserRequestBody


class UserController:

    @staticmethod
    def activate_users(user_id: UUID):
        return

    @staticmethod
    def deactivate_users(user_id: UUID):
        return

    @staticmethod
    def all_active_users(db: Session ):
        users = UserRepository.get_all_active_users(db)
        all_active_users = [UserResponse(id=user.id, name=user.name, role=user.role.name) for user in users]
        return all_active_users
    @staticmethod
    def all_inactive_users(db: Session ):
        users = UserRepository.get_all_inactive_users(db)
        all_inactive_users = [UserResponse(id=user.id, name=user.name, role=user.role.name) for user in users]
        return all_inactive_users

    @staticmethod
    def all_inactive_authors(db: Session):
        users = UserRepository.get_all_inactive_authors(db)
        all_inactive_authors = [UserResponse(id=user.id, name=user.name, role=user.role.name) for user in users]
        return all_inactive_authors

    @staticmethod
    def get_user_py_id(db: Session, user_id: UUID):
        user = UserRepository.get_user_by_id(db, user_id)
        return UserResponseModel(id=user.id, username=user.username, name=user.name, role=user.role.name)

    @staticmethod
    def stor(db, user_request: UserRequestBody):

        created_user = UserServices.create_user(db, user_request)

        return UserResponseModel(
                id=str(created_user.id),
                name=created_user.name,
                username=created_user.username,
                role=str(created_user.role.name),)

    @staticmethod
    def update(db: Session, user_id: UUID, user_request: UpdateUserRequestBody):

        updated_user = UserServices.update_user(db, user_id, user_request)

        return UserResponseModel(
            id=str(updated_user.id),
            name=updated_user.name,
            username=updated_user.username,
            role=str(updated_user.role.name), )

    @staticmethod
    def destroy(db: Session, user_id: UUID):
        user = UserRepository.get_user_by_id(db, user_id)
        if user is None:
            raise NotFoundException(f'User with {user_id} not found')
        UserRepository.delete_user_by_id(db, user_id)
        return {'message': 'User deleted successfully'}

