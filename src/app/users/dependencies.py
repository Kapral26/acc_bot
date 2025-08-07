import logging

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.app.users.chats.service import ChatsService
from src.app.users.repository import UserRepository
from src.app.users.roles.service import RolesService
from src.app.users.service import UserService


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_repository(
        self,
        logger: logging.Logger,
        session_factory: async_sessionmaker
    ) -> UserRepository:
        return UserRepository(
            session_factory=session_factory,
            logger=logger,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_service(
        self,
        user_repository: UserRepository,
        chat_service: ChatsService,
        role_service: RolesService,
    ) -> UserService:
        return UserService(
            user_repository=user_repository,
            chat_service=chat_service,
            role_service=role_service,
        )
