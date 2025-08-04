from dataclasses import dataclass

from src.app.users.chats.service import ChatsService
from src.app.users.exceptions import UserAlreadyRegisterIntoThisChat
from src.app.users.repository import UserRepository
from src.app.users.roles.service import RolesService
from src.app.users.schemas import UserSchema, UsersCreateSchema, UsersSchemaWithoutChat


@dataclass
class UserService:
    user_repository: UserRepository
    chat_service: ChatsService
    role_service: RolesService

    async def create_user(self, user_data: UsersCreateSchema) -> None:
        user_exist_into_chat = await self.chat_service.is_user_in_chat(
            user_data.id, user_data.chat.id
        )
        if user_exist_into_chat:
            raise UserAlreadyRegisterIntoThisChat
        await self.user_repository.create_user(user_data)

    async def get_users(self) -> list[UserSchema]:
        users = await self.user_repository.get_users()
        return [UserSchema.model_validate(x) for x in users]

    async def get_user_by_username(self, username: str) -> UserSchema:
        user = await self.user_repository.get_user_by_username(username)
        return UserSchema.model_validate(user)

    async def get_random_user(self, chat_id: int) -> UsersSchemaWithoutChat:
        user = await self.user_repository.get_random_user(chat_id)
        return UsersSchemaWithoutChat.model_validate(user)
