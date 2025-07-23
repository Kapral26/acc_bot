from dataclasses import dataclass

from app.roles.repository import RolesRepository
from app.roles.schemas import RoleCRUD, RoleSchema


@dataclass
class RolesService:
    roles_repository: RolesRepository

    async def create_role(self, role: RoleCRUD) -> RoleSchema:
        new_role = await self.roles_repository.create_role(role)
        return RoleSchema.model_validate(new_role)

    async def get_role_by_name(self, role_name: str):
        role = await self.roles_repository.get_roles_by_name(role_name)
        return role

    async def get_role_by_id(self, role_id: int) -> RoleSchema:
        role = await self.roles_repository.get_roles_by_id(role_id)
        return RoleSchema.model_validate(role)

    async def get_roles(self) -> list[RoleSchema]:
        roles = await self.roles_repository.get_roles()
        return [RoleSchema.model_validate(x) for x in roles]

    async def update_role(self, role_id:int, role: RoleCRUD):
        db_role = await self.roles_repository.update_role(role_id, role)
        return RoleSchema.model_validate(db_role)

    async def delete_role(self, role_id: int):
        await self.roles_repository.delete_role(role_id)
