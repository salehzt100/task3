from uuid import UUID

from sqlalchemy.orm import Session

from app import models
from app.enums import RoleEnum
from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def activate_user(self, user):
        user.is_active = True
        self.db.commit()
        self.db.refresh(user)
        return user

    def inactivate_user(self, user):
        user.is_active = False
        self.db.commit()
        self.db.refresh(user)
        return user



    def get_all_active_users(self):
        return (self.db.query(User)
                .filter(User.is_active == True)
                .all())

    def get_all_inactive_users(self):
        return (self.db.query(User)
                .filter(User.is_active == False)
                .all())

    def get_all_inactive_authors(self):
        return (self.db.query(User)
                .filter(User.is_active == False)
                .filter(User.role_id == RoleEnum.AUTHOR.value)
                .all())

    def create_user(self, user: User):
        """
        Add a new user to the database.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User):
        self.db.commit()
        self.db.refresh(user)

    def check_duplicate_username(self, user_id: UUID, username: str):
        return (self.db.query(models.User)
                .filter(User.username == username)
                .filter(User.id != user_id)
                .first())

    def check_exists_username(self, username: str):
        return (self.db.query(models.User)
                .filter(User.username == username)
                .first())

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
