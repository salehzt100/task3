from sqlalchemy.orm import Session

from app.repositories.role_repository import RoleRepository


class RoleServices:
    def __init__(self, db: Session):
        self.db = db
        self.role_repository = RoleRepository(db)


