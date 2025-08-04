from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.users.roles.dependencies import get_roles_service
from src.app.users.roles.schemas import RoleSchema
from src.app.users.roles.service import RolesService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


# Получить все роли
@router.get("/", response_model=list[RoleSchema])
async def get_roles(
    roles_service: Annotated[RolesService, Depends(get_roles_service)],
):
    roles = await roles_service.get_roles()
    return roles
