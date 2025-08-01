from dataclasses import dataclass

from app.users.chats.repository import ChatsRepository
from app.users.exceptions import UserAlreadyRegisterIntoThisChat
from app.users.repository import UserRepository
from app.users.roles.repository import RolesRepository
from app.users.schemas import UserSchema, UsersCreateSchema


@dataclass
class UserService:
    user_repository: UserRepository
    chat_repository: ChatsRepository
    role_repository: RolesRepository

    async def create_user(
            self,
            user_data: UsersCreateSchema
    ) -> None:
        user_in_chat = await self.chat_repository.is_user_in_chat(user_data.id, user_data.chat.id)

        if user_in_chat:
            raise UserAlreadyRegisterIntoThisChat

        await self.user_repository.create_user(user_data)


    async def get_users(self) -> list[UserSchema]:
        users = await self.user_repository.get_users()
        return [UserSchema.model_validate(x) for x in users]

    async def get_user_by_username(self, username: str) -> UserSchema:
        user = await self.user_repository.get_user_by_username(username)
        return UserSchema.model_validate(user)

