from src.app.russian_roulette_analytics.bad_phrase.handlers import (
    router as bad_phrase_routers,
)
from src.app.russian_roulette_analytics.handlers import router as user_routers
from src.app.users.chats.handlers import router as chats_routers
from src.app.users.handlers import router as analytics_routers
from src.app.users.roles.handlers import router as roles_routers

all_routers = [
    user_routers,
    roles_routers,
    analytics_routers,
    bad_phrase_routers,
    chats_routers,
]
