from dataclasses import dataclass

from app.users.models import User
from app.users.repository import UserRepository
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
