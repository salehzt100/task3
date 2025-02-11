from datetime import datetime
from pydantic.v1 import UUID4
from sqlalchemy.orm import Session
from app.models import User, PersonalAccessToken


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        """
        Add a new user to the database.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str):
        """
        Get user by username from database.

        """
        return self.db.query(User).filter(User.username == username).first()

    def add_token(self, token: PersonalAccessToken):
        """
        Add a new token to the database.
        """
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def delete_token(self, token: PersonalAccessToken):
        """
        Delete token from database.
        """
        self.db.delete(token)
        self.db.commit()

    def get_active_token(self, user_id: UUID4):
        """
        Get active token for user.
        """
        return (self.db.query(PersonalAccessToken)
                .filter(PersonalAccessToken.user_id == user_id)
                .filter(PersonalAccessToken.expires_at > datetime.now())
                .first())

    def check_exist_token(self, token: str) :
        return (self.db.query(PersonalAccessToken)
         .filter(PersonalAccessToken.token == token)
         .filter(PersonalAccessToken.expires_at > datetime.now())
         .first())


