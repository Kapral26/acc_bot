import logging

from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.task_manager.worker import broker


@broker.task
@inject(patch_module=True)
async def task_collect_analytics(
    callback: CallbackQuery
):
    print(f"collect analytic: {callback.message.from_user.id}")
