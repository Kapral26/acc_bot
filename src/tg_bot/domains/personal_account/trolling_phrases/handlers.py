from aiogram import Bot, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from src.tg_bot.domains.personal_account.trolling_phrases import trolling_phrases_router
from src.tg_bot.domains.personal_account.trolling_phrases.keyboards import (
    get_after_preview_inline_keyboard,
    get_phrases_keyboards,
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
    • 📁 <i>Просмотр архива</i>
    (Тебе делать хуй?)
    • ⚙️ <i>Добавление новой</i>
    (спасибо, что не в наш чат)
    • 🗑️ <i>Удаление</i>
    (наконец-то адекватный выбор)

    <i>▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬</i>  
    <code>⚠️ Внимание: Я подключил ИИ - так что нахуй иди.</code>  
    """
    await callback.message.edit_text(
        message,
        parse_mode="HTML",
        reply_markup=await get_trolling_phrases_inline_keyboard(),
    )


class TrollingPhrasesStates(StatesGroup):
    WAITING_FOR_PHRASE = State()


@trolling_phrases_router.callback_query(F.data == "add_phrase")
async def start_adding_phrase(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("📝 Введи новую троллинговую фразу:")
    await state.set_state(TrollingPhrasesStates.WAITING_FOR_PHRASE)


@trolling_phrases_router.message(TrollingPhrasesStates.WAITING_FOR_PHRASE)
@inject
async def handle_preview_new_phrase(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
    trolling_phrases_service: FromDishka[TrollingPhrasesService],
):
    try:
        preview_phrase = await trolling_phrases_service.preview_phrase(
            message.text, message.from_user.username
        )
    except ValueError as e:
        await message.answer(
            str(e),
            reply_markup=await get_trolling_phrases_inline_keyboard(),
        )
    else:
        await message.answer(
            preview_phrase, reply_markup=await get_after_preview_inline_keyboard()
        )

    await state.clear()


@trolling_phrases_router.callback_query(F.data == "add_previewed_phrase")
@inject
async def add_previewed_phrase(
    callback: CallbackQuery,
    trolling_phrases_service: FromDishka[TrollingPhrasesService],
):
    await callback.answer()

    # Сохраняем фразу
    try:
        await trolling_phrases_service.add_phrase(callback.message.text)
    except ValueError as e:
        await callback.message.edit_text(
            str(e),
            reply_markup=await get_trolling_phrases_inline_keyboard(),
        )
    else:
        # Возвращаемся в меню
        await callback.message.edit_text(
            f"✅ Фраза добавлена: <i>{callback.message.text}</i>", parse_mode="HTML"
        )
        await callback.message.answer(
            "Выберите действие:",
            reply_markup=await get_trolling_phrases_inline_keyboard(),
        )


# --
PHRASES_PER_PAGE = 5


@trolling_phrases_router.callback_query(F.data == "all_phrases")
@inject
async def show_first_page(
    callback: CallbackQuery,
    trolling_phrases_service: FromDishka[TrollingPhrasesService],
):
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

    await callback.message.edit_text(
        message_text,
        parse_mode="HTML",
        reply_markup=await get_phrases_keyboards(page, total_pages),
    )
