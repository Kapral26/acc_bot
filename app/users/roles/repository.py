from app.users.roles.schemas import RoleKey, RoleSchema, RoleValue


class RolesRepository:
    async def get_role_name_by_id(self, role_id: int) -> str:
        role_key = RoleKey(role_id)
        role_name = RoleValue[role_key.name].value
        return role_name

    async def get_role_id_by_name(self, role_name: str) -> int:
        role_value = RoleValue(role_name)
        role_name = RoleKey[role_value.name].value
        return role_name

    async def get_roles(self) -> list[RoleSchema]:
        all_roles = [
            RoleSchema(id=role.value, name=RoleValue[role.name].value)
            for role in RoleKey
        ]
        return all_roles
