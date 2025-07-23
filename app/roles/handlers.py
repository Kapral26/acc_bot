
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.dependencies import get_roles_service
from app.roles.schemas import RoleSchema, RoleCRUD
from app.roles.service import RolesService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)

# Получить все роли
@router.get("/", response_model=list[RoleSchema])
async def get_roles(
roles_service: Annotated[RolesService, Depends(get_roles_service)],
):
    try:
        roles = await roles_service.get_roles()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return roles

# Получить одну роль по id
@router.get("/by-id/{role_id}", response_model=RoleSchema)
async def get_role_by_id(role_id: int, roles_service: Annotated[RolesService, Depends(get_roles_service)],):
    try:
        roles = await roles_service.get_role_by_id(role_id)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return roles

@router.get("/by-name/{role_name}", response_model=RoleSchema)
async def get_role_by_name(role_name: str, role_service: Annotated[RolesService, Depends(get_roles_service)]):
    try:
        role = await role_service.get_role_by_name(role_name)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return role

# Создать новую роль
@router.post("/", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
async def create_role(
        role: RoleCRUD,
        roles_service: Annotated[RolesService, Depends(get_roles_service)]
):
    try:
        roles = await roles_service.create_role(role)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return roles

# Обновить роль
@router.put("/{role_id}", response_model=RoleSchema, status_code=status.HTTP_200_OK)
async def update_role(role_id:int,  role: RoleCRUD, roles_service: Annotated[RolesService, Depends(get_roles_service)]):
    try:
        roles = await roles_service.update_role(role_id, role)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return roles


# Удалить роль
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, roles_service: Annotated[RolesService, Depends(get_roles_service)]):
    try:
        await roles_service.delete_role(role_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
