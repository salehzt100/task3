from fastapi.params import Depends
from sqlalchemy.orm import Session

from bootstrap import get_db
from database.schema import RegisterRequestBody
from utils import exception_handler
from ..repositories.auth_repository import AuthRepository
from ..services import AuthService


class AuthController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.auth_services = AuthService(db)
        self.auth_repository = AuthRepository(db)

    @exception_handler
    def register(self, user: RegisterRequestBody):
        """
        Register a new user.
        """
        return self.auth_services.register_user(user)

    @exception_handler
    def login(self, username: str, password: str):
        """
        Login with username and password.
        """
        return self.auth_services.login_user(username, password)

    @exception_handler
    def get_user_by_username(self, username: str):
        """
        Get a user by their username.
        """
        return self.auth_repository.get_user_by_username(username)

    @exception_handler
    def get_personal_access_token(self, token: str):
        """
        Check if the provided token exists and return it.
        """
        token = self.auth_repository.check_exist_token(token)
        print('token in controller:', token)  # Log the token (for debugging purposes)
        return token
