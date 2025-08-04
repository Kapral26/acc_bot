from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.app.users.roles.schemas import RoleSchema
from src.app.users.roles.service import RolesService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


# Получить все роли
@router.get("/", response_model=list[RoleSchema])
@inject
async def get_roles(
    roles_service: FromDishka[RolesService],
):
    roles = await roles_service.get_roles()
    return roles
