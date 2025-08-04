from typing import Annotated

from fastapi import Depends

from src.app.users.roles.repository import RolesRepository
from src.app.users.roles.service import RolesService


async def get_roles_repository() -> RolesRepository:
    return RolesRepository()


def get_roles_service(
    roles_repository: Annotated[RolesRepository, Depends(get_roles_repository)],
) -> RolesService:
    return RolesService(roles_repository=roles_repository)
