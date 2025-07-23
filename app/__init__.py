from app.roles.handlers import router as roles_routers
from app.users.handlers import router as user_routers

all_routers = [
    user_routers,
    roles_routers
]
