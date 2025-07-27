from dataclasses import dataclass

from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserSchema, UsersCreateSchema


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(
            self,
            user_data: UsersCreateSchema
    ) -> None:
       await self.user_repository.create_user(
            user_data
        )


    async def get_users(self) -> list[UserSchema]:
        users = await self.user_repository.get_users()
        return [UserSchema.model_validate(x) for x in users]

    async def get_user_by_username(self, username: str) -> UserSchema:
        user = await self.user_repository.get_user_by_username(username)
        return UserSchema.model_validate(user)

    async def set_user_to_admin(self, username: str, chat_id: int):
        user = await self.user_repository.get_user_by_username(username)
        await self.user_repository.set_user_to_admin(user.id, chat_id)
