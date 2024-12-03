from sqlalchemy.orm import Session
from database.schema import RegisterRequestBody
from ..services import AuthService

class AuthController:
    @staticmethod
    def register(user: RegisterRequestBody, db: Session):
        """
        Register a new user.
        """
        return AuthService.register_user(user, db)

    @staticmethod
    def login(username,password, db: Session):
        """
        Register a new user.
        """
        return AuthService.login_user(username,password, db)






