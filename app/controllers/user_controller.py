from uuid import UUID
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.user_services import UserServices
from bootstrap import get_db
from database import UserResponseModel
from database.schema import UserResponse, UpdateUserRequestBody, AddUserRequestBody
from utils import exception_handler


class UserController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_repository = UserRepository(db)
        self.user_services = UserServices(db)

    @exception_handler
    def activate_users(self, user_id: UUID):
        """
        Activate a user by their ID.
        """
        user = self.user_services.activate_user(user_id)
        return {
            'message': 'User activated successfully',
            'user': self.user_response(user)
        }

    @exception_handler
    def inactivate_users(self, user_id: UUID):
        """
        Inactivate a user by their ID.
        """
        user = self.user_services.inactivate_user(user_id)
        return {
            'message': 'User inactivated successfully',
            'user': self.user_response(user)
        }

    @exception_handler
    def deactivate_users(self, user_id: UUID):
        """
        Deactivate a user by their ID.
        """
        # Placeholder for deactivating a user. Functionality can be added.
        pass

    @exception_handler
    def all_active_users(self):
        """
        Retrieve all active users.
        """
        users = self.user_repository.get_all_active_users()
        return [self.user_response(user) for user in users]

    @exception_handler
    def all_inactive_users(self):
        """
        Retrieve all inactive users.
        """
        users = self.user_repository.get_all_inactive_users()
        return [self.user_response(user) for user in users]

    @exception_handler
    def all_inactive_authors(self):
        """
        Retrieve all inactive authors.
        """
        users = self.user_repository.get_all_inactive_authors()
        return [self.user_response(user) for user in users]

    @exception_handler
    def get_user_by_id(self, user_id: UUID):
        """
        Retrieve a user by their ID.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(f'User with id {user_id} not found')
        return self.user_response_model(user)

    @exception_handler
    def store(self, user_request: AddUserRequestBody):
        """
        Create a new user.
        """
        created_user = self.user_services.create_user(user_request)
        return self.user_response_model(created_user)

    @exception_handler
    def update(self, user_id: UUID, user_request: UpdateUserRequestBody):
        """
        Update an existing user's information.
        """
        updated_user = self.user_services.update_user(user_id, user_request)
        return self.user_response_model(updated_user)

    @exception_handler
    def destroy(self, user_id: UUID):
        """
        Delete a user by their ID.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(f'User with {user_id} not found')

        self.user_repository.delete_user(user)
        return {'message': 'User deleted successfully'}

    @exception_handler
    def user_response(self, user: User):
        """
        Format the user data into a response.
        """
        return UserResponse(
            id=user.id,
            name=user.name,
            role=user.role.name
        )

    @exception_handler
    def user_response_model(self, user: User):
        """
        Format the user data into a model response.
        """
        return UserResponseModel(
            id=str(user.id),
            name=user.name,
            username=user.username,
            role=str(user.role.name),
        )
