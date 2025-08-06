from aiogram import Bot, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.personal_account.trolling_phrases import trolling_phrases_router
from src.tg_bot.domains.personal_account.trolling_phrases.keyboards import (
    get_trolling_phrases_inline_keyboard,
)
from src.tg_bot.domains.personal_account.trolling_phrases.services import (
    TrollingPhrasesService,
)


@trolling_phrases_router.callback_query(F.data == "trolling_phrases")
@inject
async def handle_trolling_phrases(callback: CallbackQuery):
    await callback.answer("Блять ну ты и мудень...")
    message = """
    <b>🔧 ФУНКЦИОНАЛ 🔧</b>

    <i>▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</i>
    • 📁 <i>Просмотр архива</i> (Тебе делать хуй?)
    • ⚙️ <i>Добавление новой</i> (спасибо, что не в наш чат)
    • 🗑️ <i>Удаление</i> (наконец-то адекватный выбор)

    <i>▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</i>  
    <code>⚠️ Внимание: Я подключил ИИ - так что нахуй иди.</code>  
    """
    await callback.message.edit_text(
        message,
        parse_mode="HTML",
        reply_markup=await get_trolling_phrases_inline_keyboard(),
    )


PHRASES_PER_PAGE = 5


@trolling_phrases_router.callback_query(F.data == "all_phrases")
@inject
async def show_first_page(
    callback: CallbackQuery,
    trolling_phrases_service: FromDishka[TrollingPhrasesService],
):
    # Вместо создания нового CallbackQuery, просто вызываем обработчик страницы
    await _handle_phrases_page(callback, trolling_phrases_service, page=1)


@trolling_phrases_router.callback_query(F.data.startswith("phrases_page_"))
@inject
async def handle_phrases_page(
    callback: CallbackQuery,
    bot: Bot,
    trolling_phrases_service: FromDishka[TrollingPhrasesService],
    page: int | None = None,
):
    if page is None:
        page = int(callback.data.split("_")[-1])
    await _handle_phrases_page(callback, trolling_phrases_service, page)


async def _handle_phrases_page(
    callback: CallbackQuery,
    trolling_phrases_service: TrollingPhrasesService,
    page: int | None = None,
):
    await callback.answer("Листаем...")
    phrases = await trolling_phrases_service.get_all_phrases()
    total_pages = (len(phrases) + PHRASES_PER_PAGE - 1) // PHRASES_PER_PAGE
    # Получаем фразы для текущей страницы
    start_idx = (page - 1) * PHRASES_PER_PAGE
    end_idx = start_idx + PHRASES_PER_PAGE
    current_phrases = [x["phrase"] for x in phrases[start_idx:end_idx]]
    # Формируем текст сообщения
    message_text = "<b>📜 Все фразы:</b>\n\n"
    for i, phrase in enumerate(current_phrases, start=start_idx + 1):
        message_text += f"{i}. <code>{phrase}</code>\n"
    message_text += f"\nСтраница {page}/{total_pages}"
    # Создаем клавиатуру с пагинацией
    builder = InlineKeyboardBuilder()
    # Кнопки пагинации
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"phrases_page_{page - 1}")
    if page < total_pages:
        builder.button(text="Вперед ➡️", callback_data=f"phrases_page_{page + 1}")
    # Кнопка возврата
    builder.button(text="🔙 Назад", callback_data="trolling_phrases")
    builder.adjust(2)  # Группируем кнопки пагинации
    await callback.message.edit_text(
        message_text, parse_mode="HTML", reply_markup=builder.as_markup()
    )
