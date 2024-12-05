from sqlalchemy.orm import Session

from app import models


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
