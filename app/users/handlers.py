from typing import Annotated

from starlette import status

from app.dependencies import get_user_service
from app.users.exceptions import UserWasExits
from app.users.schemas import UserSchema, UsersCreateSchema, \
    UserWasCreated
from app.users.service import UserService
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserWasCreated, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UsersCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        await user_service.create_user(user_data)
    except UserWasExits as e:
        raise HTTPException(status_code=409, detail="Ты дурак? Ты уже зарегистрирован")
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    else:
        return UserWasCreated()


@router.get("/", response_model=list[UserSchema])
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> list[UserSchema]:
    try:
        users = await user_service.get_users()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return users

@router.patch("/{username}/to-admin")
async def set_user_to_admin(
        username: str,
        chat_id: int,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserSchema:
    await user_service.set_user_to_admin(username, chat_id)
