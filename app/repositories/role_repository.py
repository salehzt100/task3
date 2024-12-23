from sqlalchemy.orm import Session

from app.models import Role


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self):
        return self.db.query(Role).all()