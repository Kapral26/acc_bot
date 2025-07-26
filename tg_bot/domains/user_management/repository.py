from dataclasses import dataclass

from app.users.schemas import UsersCreateSchema
from tg_bot.domains.api_adapter.service import APIAdapter


@dataclass
class UserBotRepository:
    api_adapter: APIAdapter

    async def register_user(self, user_data: UsersCreateSchema):
        await self.api_adapter.api_post(
            "http://localhost:8000/users/",
            data=user_data.model_dump(mode="json"))


    async def change_role(self, user_data: UsersCreateSchema):
        await self.api_adapter.api_post(
            "http://localhost:8000/users/", data=user_data.model_dump(mode="json")
        )
# a = {
#     "chat":
#         {
#             "id": 471077141,
#             "title": None,
#             "type": "private"
#         },
#     "first_name": "kapral26",
#     "last_name": None,
#     "role_id": 3,
#     "username": "kapral26"
# }
