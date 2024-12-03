from typing import List

from fastapi import APIRouter

from database.schema import RoleResponse, RoleRequestBody

router = APIRouter(tags=["Roles"])

''' ROLES APIs '''
@router.get('/roles', response_model=List[RoleResponse])
async def list_role():
    pass

@router.get('/roles/{role_id}', response_model=RoleResponse)
async def show_role(role_id: int):
    pass

@router.post('/roles', response_model=RoleResponse)
async def create_role(role_body: RoleRequestBody):
    pass

@router.put('/roles/{role_id}', response_model=RoleResponse)
async def update_role(role_id: int, role_body: RoleRequestBody):
    pass

@router.delete('/roles/{role_id}', response_model=dict)
async def delete_role(role_id: int):
    pass
