from app import all_routers
from fastapi import FastAPI

app = FastAPI()

for router in all_routers:
    app.include_router(router)