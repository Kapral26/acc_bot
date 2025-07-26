from dataclasses import dataclass

from app.users.models import User
from app.users.repository import UserRepository
from app.users.roles.schemas import RoleCRUD
from app.users.schemas import UserSchema


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(
            self,
            username: str,
            first_name: str,
            last_name: str
    ) -> UserSchema:
        new_user: User = await self.user_repository.create_user(
            username,
            first_name,
            last_name
        )
        new_user: UserSchema = UserSchema.model_validate(new_user)
        return new_user

    async def get_users(self) -> list[UserSchema]:
        users = await self.user_repository.get_users()
        return [UserSchema.model_validate(x) for x in users]

    async def get_user_by_username(self, username: str) -> UserSchema:
        user = await self.user_repository.get_user_by_username(username)
        return UserSchema.model_validate(user)

    async def update_user_role(self, username: str, new_role: RoleCRUD) -> None:
        user = await self.user_repository.get_user_by_username(username)
        a = 1
        # TODO Проверить
