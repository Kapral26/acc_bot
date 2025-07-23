from app.analytics.bad_phrase.handlers import router as bad_phrase_routers
from app.analytics.handlers import router as user_routers
from app.roles.handlers import router as roles_routers
from app.users.handlers import router as analytics_routers

all_routers = [
    user_routers,
    roles_routers,
    analytics_routers,
    bad_phrase_routers
]
