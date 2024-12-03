from datetime import datetime

from pydantic.v1 import UUID4
from sqlalchemy.orm import Session
from app.models import User, PersonalAccessToken


class AuthRepository:

    @staticmethod
    def create_user(db: Session, user: User):
        """
        Add a new user to the database.
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    @staticmethod
    def get_user_by_username(db: Session, username: str):
        """
        get user by username from  database.
        """
        return db.query(User).filter(User.username == username).first()


    @staticmethod
    def add_token(db: Session, token: PersonalAccessToken):
        """
        Add a new token to the database.
        """
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    @staticmethod
    def get_active_token(db: Session, user_id: UUID4):
        """
        get active token for user.
        """
        return (db.query(PersonalAccessToken)
                .filter(PersonalAccessToken.user_id == user_id)
                .filter(PersonalAccessToken.expires_at > datetime.now())
                .first())
