import hashlib

from sqlalchemy.orm import Session
from models import User
from schema import RegisterRequestBody


class AuthController:

    @staticmethod
    def register(user: RegisterRequestBody, db: Session):
        try:
            new_user = User(
                name=user.name,
                username=user.username,
                password=hashlib.sha256(user.password.encode('utf-8')).hexdigest(),
                role_id=user.role_id.value,
                is_active=True if user.role_id == 1 else False,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            db.rollback()  # Rollback on exception
            return {"error": str(e)}
        finally:
            db.close()  # Always close the session


