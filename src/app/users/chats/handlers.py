from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from src.app.users.chats.schemas import UserChatSchema
from src.app.users.chats.service import ChatsService
from src.app.users.exceptions import UserIsNotRegisteredIntoThisChat

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@router.get("/", response_model=list[UserChatSchema])
@inject
async def get_chats(
    chats_service: FromDishka[ChatsService],
):
    try:
        chats = await chats_service.get_chats()
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))
    return chats


@router.get("/{chat_id}", response_model=UserChatSchema)
@inject
async def get_chat_by_id(
    chat_id: int,
    chats_service: FromDishka[ChatsService],
):
    try:
        chat = await chats_service.get_chat_by_id(chat_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return chat


@router.get("/by-title/{title}", response_model=UserChatSchema)
@inject
async def get_chat_by_title(
    title: str,
    chats_service: FromDishka[ChatsService],
):
    try:
        chat = await chats_service.get_chat_by_title(title)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))
    return chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_chat(
    chat_id: int,
    chats_service: FromDishka[ChatsService],
):
    try:
        await chats_service.delete_chat(chat_id)
    except Exception as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get(
    "/{chat_id}/users/{user_id}",
    status_code=status.HTTP_200_OK,
)
@inject
async def is_user_in_chat(
    chat_id: int,
    user_id: int,
    chat_service: FromDishka[ChatsService],
):
    user_exist_into_chat = await chat_service.is_user_in_chat(user_id, chat_id)
    if not user_exist_into_chat:
        raise UserIsNotRegisteredIntoThisChat

    return {"in_chat": True}
