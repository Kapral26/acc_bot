from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from src.app.users.schemas import UserSchema, UsersCreateSchema
from src.app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(
    user_data: UsersCreateSchema,
    user_service: FromDishka[UserService],
):
    await user_service.create_user(user_data)


@router.get("/", response_model=list[UserSchema])
@inject
async def get_users(
    user_service: FromDishka[UserService],
) -> list[UserSchema]:
    try:
        users = await user_service.get_users()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return users

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@inject
async def get_user_by_id(
        user_id: int,
        user_service: FromDishka[UserService],
):
    user_exist = await user_service.get_user_by_id(user_id)
    return {
        "user_status_exist": user_exist
    }
