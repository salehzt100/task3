from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.role_repository import RoleRepository
from app.services.role_services import RoleServices
from bootstrap import get_db
from database.schema import RoleResponse


class RoleController:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.role_services = RoleServices(db)
        self.role_repository = RoleRepository(db)

    def index(self):
        """
        Retrieve all roles.
        """
        roles = self.role_repository.get()
        return [RoleResponse(id=role.id, name=role.name) for role in roles]
