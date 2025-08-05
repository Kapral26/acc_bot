from aiogram import Bot, types
from aiogram.filters import Command
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.start_domain import start_router
from src.tg_bot.domains.start_domain.keyboards import get_start_inline_keyboard
from src.tg_bot.domains.user_management.services import UserBotService


@start_router.message(Command("start"))
@inject
async def start_command(
    message: types.Message,
    bot: Bot,
    user_bot_service: FromDishka[UserBotService],
) -> None:
    """Обработчик команды /start."""
    user = await user_bot_service.is_user_in_chat(message)

    kb = await get_start_inline_keyboard(bot, user.in_chat)
    await message.answer(
        """
*Привет!* ✌️
➡️ Иди по *известному* направлению.
🔫 Хочешь сыграть в *Русскую рулетку*? — *Зарегистрируйся!*
🤡*Личный кабинет*:
- Можно посмотреть статистику по конкретному чату.
- Добавить новые фразы.
""",
        reply_markup=kb,
        parse_mode="Markdown",  # Не забудьте включить парсинг Markdown
    )
