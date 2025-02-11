from typing import List

from fastapi import APIRouter, Depends

from app.controllers.role_controller import RoleController
from database.schema import RoleResponse
from utils.fastapi.dependencies import role_required

router = APIRouter(tags=["Roles"])

''' ROLES APIs '''


@router.get('/roles',
            response_model=List[RoleResponse],
            dependencies=[Depends(role_required(['EDITOR', 'ADMIN']))],
            )
async def list_role(role_controller: RoleController = Depends(RoleController)):
    return role_controller.index()
