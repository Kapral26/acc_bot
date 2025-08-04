import logging

from dishka import Provider, Scope, provide

from src.app.settings.database.database import async_session_factory
from src.app.users.chats.repository import ChatsRepository
from src.app.users.chats.service import ChatsService


class ChatsProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_chat_repository(self) -> ChatsRepository:
        return ChatsRepository(session_factory=async_session_factory)

    @provide(scope=Scope.REQUEST)
    async def get_chats_service(
            self,
        chats_repository: ChatsRepository,
        logger: logging.Logger,
    ) -> ChatsService:
        return ChatsService(chats_repository=chats_repository, logger=logger)
