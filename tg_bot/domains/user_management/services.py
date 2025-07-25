from aiogram import types

from .models import UserData


class UserService:
    @staticmethod
    def extract_user_data(message: types.Message) -> UserData:
        user = message.from_user
        return UserData(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat_id=message.chat.id,
        )
