from uuid import UUID

from sqlalchemy.orm import Session

from app import models
from app.enums import RoleEnum
from app.models import User


class UserRepository:
    @staticmethod
    def get_user_by_id(db: Session, user_id):
        return db.query(models.User).filter(models.User.id == user_id).first()


    @staticmethod
    def activate_user(db: Session, user_id):
        user = UserRepository.get_user_by_id(db, user_id)
        user.is_active = True
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def deactivate_user(db: Session, user_id):
        user = UserRepository.get_user_by_id(db, user_id)
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_active_users( db: Session):
        return (db.query(User)
                .filter(User.is_active == True)
                .all())


    @staticmethod
    def get_all_inactive_users(db: Session):
        return (db.query(User)
                .filter(User.is_active == False)
                .all())
    @staticmethod
    def get_all_inactive_authors(db: Session):
        return (db.query(User)
                .filter(User.is_active == False)
                .filter(User.role_id == RoleEnum.AUTHOR.value)
                .all())
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
    def update_user(db: Session, user: User):
        """
        Add a new user to the database.
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def check_duplicate_username(db: Session, user_id: UUID, username: str):
        return (db.query(models.User)
                .filter(User.username == username)
                .filter(User.id != user_id)
                .first())
    @staticmethod
    def delete_user_by_id(db: Session, user_id: UUID):
        result = db.query(models.User).filter(User.id == user_id).delete()
        db.commit()
        return result
