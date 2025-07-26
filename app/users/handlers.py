from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_user_service
from app.users.exceptions import UserWasExits
from app.users.roles.schemas import RoleCRUD
from app.users.schemas import UserSchema, UsersCreateSchema
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserSchema)
async def create_user(
    body: UsersCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserSchema:
    try:
        create_user_result = await user_service.create_user(
            username=body.username,
            first_name=body.first_name,
            last_name=body.last_name
        )
    except UserWasExits as e:
        raise HTTPException(status_code=409, detail=e.detail)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))

    return create_user_result


@router.get("/", response_model=list[UserSchema])
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> list[UserSchema]:
    try:
        users = await user_service.get_users()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return users

@router.patch("/{username}/new_role", response_model=UserSchema)
async def update_user_role(
        username: str,
        new_role: RoleCRUD,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserSchema:
    await user_service.update_user_role(username, new_role)
