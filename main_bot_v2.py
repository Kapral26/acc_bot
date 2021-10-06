# -*- coding: utf-8 -*-

"""
Бот для моего локального чата имеет множество функций
основные: Послать друга нахуй и менджемнта нашего алкокиноклуба
"""

from collections import Counter, OrderedDict
from datetime import datetime, time
from random import choice

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater, MessageHandler, CommandHandler, \
    ConversationHandler, Filters, PollAnswerHandler
from telegram.utils.request import Request

from setting.bot_setting import BotSetting, WorkWithUser, log_error, logging, chk_user
from setting.cinema import Cinema

FIND_MOVIE, FIND_DONE, FINNALY_DONE = range(3)
NEXT, DETAIL_VIEW, VIEW_ALL, FINAL_VIEW = range(4)

CALLBACK_BEGIN = 'x1'


class AlcoCinemaBot(BotSetting):
    """
    Основной класс для работы бота
    """

    def __init__(self):
        BotSetting.__init__(self)
        self.cinema = Cinema()
        self.users = WorkWithUser()
        self.chat_id = None
        self.movies = None
        self.report_go_f_self = None
        self.dict_list_movie = None
        self.list_answer = None
        self.list_cinema = None

    @chk_user
    @log_error
    def help_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /help
        """

        update.message.reply_text(
                text='''Список команд:
                /help - выведет тебе все необходимые команды
                /add добавить фильм в лист ожидания
                /viewlist - Вывести фильмы из листа ожидания
                /normalno
                /create_poll - Создать опрос, какой фильм будем смотреть
                /who_income - Создать опрос, кто планирует прийти
                /statistic (-m) (-y) - Вывести статистику
                /rus_rulet - Сыграть в хуёвую рулетку
                /get_rep_fys - Вывести статистику хуёвой рулетки
                /insert_phrase - Добавить фразу для определения направления,\n где необходимо вставить логин пользователя пишите @
                ''',
                parse_mode=ParseMode.HTML,
        )

    @chk_user
    @log_error
    def start_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /start
        """
        self.chat_id = update.message.chat_id

        context.bot.send_message(
                text=f'Бот АлкоКиноКлуба\n'
                     'Не забудь пройти по направлению\n'
                     'Чтобы посмотреть список команд:\n'
                     '/help',
                parse_mode=ParseMode.HTML,
                chat_id=self.chat_id,
        )

    @chk_user
    @log_error
    def normalno_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /normalno
        Команда посылает отправителя команды на всем известный сайт
        """
        update.message.reply_text(
                f'{update.effective_user.mention_html()}, Пошел на хуй!\n'
                'https://natribu.org/',
                disable_web_page_preview=False,
                parse_mode=ParseMode.HTML,
        )

    @chk_user
    @log_error
    def insert_main_phrase_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /insert_main_phrase
        Добавить фразу с помощью которой можно будет в русской
        рулетке послать случайного участника чата
        """
        chat_id = update.message.chat_id
        msg_text = update.message.text
        if '/insert_phrase' == msg_text or '/insert_phrase@alco_cinema_club_bot' == msg_text:
            update.message.bot.send_message(
                    chat_id=chat_id,
                    text=f'Пишите фразу после команды, место где надо вставить логин пользователя пишите @',
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END
        msg_text = msg_text.replace('/insert_phrase ', '').replace('@alco_cinema_club_bot', '')
        if '@' not in msg_text:
            update.message.bot.send_message(
                    chat_id=chat_id,
                    text=f'Пишите фразу, место где надо вставить логин пользователя пишите @',
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END

        result_insert = self.insert_main_phrase(msg_text)
        if result_insert:
            text = 'well done, фраза в обойме'
        else:
            text = 'Не, все хуйня, давай по новой'

        update.message.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    @chk_user
    @log_error
    def rus_rulet_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /rus_rulet
        Команда работает только в период 8:00-23:59
        Команда случайным образом выбирает человека и фразу из БД
        для того чтобы этот человек был послан нахуй
        """
        chat_id = update.message.chat_id

        start_period = time(8, 0, 0)
        end_period = time(23, 59, 0)
        ntime = datetime.now().time()

        if ntime <= start_period or ntime > end_period:
            user_link = update.effective_user.mention_html()
            update.message.bot.send_message(
                    chat_id=chat_id,
                    text=f'{user_link},/ К вам выехали чеченцы, ибо нехуй!\n Рулетка работает 8:00-23:59',
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END

        user_goes = self.users.get_user_for_rulet()
        logging.info(f'{user_goes[1]}')
        self.users.calc_goes_fuck_to_self(user_goes[0])
        main_word = self.users.get_main_word().format(user=user_goes[1])
        logging.info(f'{user_goes[1]}, {main_word}')

        update.message.bot.send_message(
                chat_id=chat_id,
                text=main_word,
        )

    @chk_user
    @log_error
    def get_rep_fys_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /get_rep_fys
        Вывести статистику кто сколько раз был послан нахуй
        """
        user_role = self.users.chk_role_user(update.effective_user.username)
        user_link = update.effective_user.mention_html()
        if user_role:
            context.bot.send_message(
                    text=f'{user_link}, это сделано не для тебя и не для таких как ты!',
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END

        report_text = self.users.get_report_fys()
        chat_id = update.message.chat_id

        update.message.bot.send_message(
                chat_id=chat_id,
                text=report_text,
                parse_mode=ParseMode.HTML,
        )

    @chk_user
    @log_error
    def add_handler(self, update: Update, context: CallbackContext):
        """
        обработчик команды /add
        """
        chat_id = update.message.chat_id

        update.message.bot.send_message(
                chat_id=chat_id,
                text='Введи название фильма:',
        )
        return FIND_MOVIE

    @log_error
    def find_movie_handler(self, update: Update, context: CallbackContext):
        """
        Поиск фильма по введенному названию

        """
        if update.message.text == '/cancel':
            return ConversationHandler.END

        self.movies = self.cinema.find_cinema(update.message.text)

        find_keyboard = [
            [InlineKeyboardButton(text=f"{x['title']}({x['year']})", callback_data=x['id'])] for x in
            self.movies
        ]

        find_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel')])

        inline_buttons = InlineKeyboardMarkup(
                inline_keyboard=find_keyboard,
        )

        update.message.reply_text(
                text=f'Выбери фильм, который необходимо добавить:',
                reply_markup=inline_buttons,
        )
        return FIND_DONE

    @log_error
    def find_done_handler(self, update: Update, context: CallbackContext):
        """
        Обраобтчик действий выбранного фильма
        """

        if update.callback_query.data == 'cancel':
            context.bot.send_message(
                    text='Отмена.\nЧтобы начать сначала введите: /add',
                    chat_id=update.effective_chat.id
            )
            return ConversationHandler.END

        movie_id = int(update.callback_query.data)
        movie_data = [x for x in self.movies if x['id'] == movie_id][0]
        movie_data['user_pk'] = self.users.chk_users(username=update.effective_chat.username)
        context.user_data[FIND_DONE] = movie_data

        inline_buttons = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Добавить в список на просмотр', callback_data='add_list_view')],
                    [InlineKeyboardButton(text='Посмотрели мы фильм сей', callback_data='was_viewed')]
                ],
        )

        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"""Че по фильму "{movie_data['title']} ({movie_data['year']})" ?""",
                reply_markup=inline_buttons,
        )

        return FINNALY_DONE

    def finally_find_done(self, update: Update, context: CallbackContext):
        """
        Обраотчик кнопок при итоговом выборе фильма
        """
        movie_data = context.user_data[FIND_DONE]
        text_done = None

        if update.callback_query.data == 'add_list_view':

            save_result = self.cinema.insert_cinema(movie_data)

            if isinstance(save_result, str):
                text_done = save_result
            else:
                text_done = f'''Все данные успешно сохранены!\nФильм: "{movie_data['title']}"\nдобавлен в список'''

        if update.callback_query.data == 'was_viewed':

            save_result = self.cinema.insert_cinema(movie_data, is_watch=True)

            if isinstance(save_result, str):
                text_done = save_result
            else:
                text_done = f'''Пожайлуй да\nФильм: "{movie_data['title']}"\nмы уже смотрели'''

        # Завершить диалог
        update.effective_message.reply_text(
                text=text_done,
        )
        return ConversationHandler.END

    @log_error
    def cancel_handler(self, update: Update, context: CallbackContext):
        """
        Отменить весь процесс диалога. Данные будут утеряны
        """
        update.message.reply_text('Отмена.\nЧтобы начать сначала введите: /add')
        return ConversationHandler.END

    @chk_user
    @log_error
    def viewlist_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик команды /viewlist
        Вывести список фильмав, которые в очереди на просмотр
        """
        self.dict_list_movie = self.cinema.view_list()
        count_view = 10

        buttons_view = [
            [InlineKeyboardButton(text=f"{x['title']} ({x['movie_year']})", callback_data=f"d;{x['id']}")] for x
            in self.dict_list_movie[:count_view]
        ]

        buttons_view.append([InlineKeyboardButton(text='->', callback_data=count_view)])

        inline_buttons = InlineKeyboardMarkup(
                inline_keyboard=buttons_view
        )

        update.message.reply_text(
                text='Список фильмов:',
                reply_markup=inline_buttons,
        )

        return NEXT

    @log_error
    def viewlist_next_handler(self, update: Update, context: CallbackContext):
        """
        Обработчик кнопки -> в команде /viewlist
        """
        callback_view = update.callback_query
        callback_view.answer()
        if callback_view.data == 'all':
            return VIEW_ALL

        if 'd;' in callback_view.data:
            context.user_data[DETAIL_VIEW] = int(callback_view.data.split(';')[1])
            return DETAIL_VIEW

        count_view = int(update.callback_query.data)
        count_view_next = count_view + 10  # 10

        buttons_view = [
            [InlineKeyboardButton(text=f"{x['title']} ({x['movie_year']})", callback_data=f"d;{x['id']}")] for x
            in self.dict_list_movie[count_view:count_view_next]
        ]

        buttons_view.append([InlineKeyboardButton(text='->', callback_data=count_view_next)])

        inline_buttons = InlineKeyboardMarkup(
                inline_keyboard=buttons_view
        )

        if not self.dict_list_movie[count_view:count_view_next]:
            context.bot.send_message(
                    text='Весь список на экране',
                    chat_id=update.effective_chat.id
            )
            return ConversationHandler.END

        context.bot.send_message(
                text='Вот тебе еще пачка фильмов',
                chat_id=update.effective_chat.id,
                reply_markup=inline_buttons,
        )

        return NEXT

    @log_error
    def viewlist_detail_handler(self, update: Update, context: CallbackContext):

        movie_id = context.user_data[DETAIL_VIEW]
        text_detail_movie = self.cinema.movie_detail(movie_id)
        buttons = [('Добавить в опрос', 'add'),
                   ('Посмотрели', 'watched'),
                   ('Заебись инфа', 'close')]

        inline_buttons = InlineKeyboardMarkup(
                inline_keyboard=[

                    [InlineKeyboardButton(text=f"{x[0]}", callback_data=x[1])] for x in
                    buttons

                ],
        )

        context.bot.send_message(
                text=text_detail_movie,
                chat_id=update.effective_chat.id,
                reply_markup=inline_buttons,
        )
        return FINAL_VIEW

    def viewlist_filnal_handler(self, update: Update, context: CallbackContext):

        message = None
        col_detail = update.callback_query.data
        movie_id = context.user_data[DETAIL_VIEW]
        if col_detail == 'close':
            return ConversationHandler.END
        elif col_detail == 'add':
            message = self.cinema.to_poll(movie_id)
        elif col_detail == 'watched':
            message = self.cinema.mark_viewed(movie_id)

        context.bot.send_message(
                text=message,
                chat_id=update.effective_chat.id,
        )

        return ConversationHandler.END

    @log_error
    def viewlist_all_handler(self, update: Update, context: CallbackContext):
        preint_text = [f">>\nНазвание Фильма: {x['title']}\nГод: {x['movie_year']}\n Рейтинг: {x['rating']}" for x in
                       self.dict_list_movie]

        context.bot.send_message(
                text='\n'.join(preint_text),
                chat_id=update.effective_chat.id,
                reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    @chk_user
    @log_error
    def create_poll_handler(self, update: Update, context: CallbackContext):
        user_role = self.users.chk_role_user(update.effective_user.username)
        if user_role:
            context.bot.send_message(
                    text=f'{update.effective_user.mention_html()}, ты челядь, негоже тебе опросы создавать',
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END

        questions = self.cinema.for_create_poll()
        if len(questions) < 2:
            context.bot.send_message(
                    text="Нехуй Вам любезный, предложить.\n воспользуйтесь командой \\add",
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END
        message = context.bot.send_poll(
                update.effective_chat.id,
                f"Псс, ребзи в среду({self.next_wednesday()}) собираемся,\nЧто будем смотреть?",
                questions,
                is_anonymous=False,
                allows_multiple_answers=True,
                # open_period=30,
                close_date=self.next_monday(),
        )
        # Save some info about the poll the bot_data for later use in receive_poll_answer
        payload = {
            message.poll.id: {
                "questions": questions,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0,
            }
        }
        context.bot.pin_chat_message(
                chat_id=update.effective_chat.id,
                message_id=message.message_id,
        )
        context.bot_data.update(payload)

    @staticmethod
    def cinema4watch(self, list_watch):
        dict_answerrs = Counter(list_watch)
        ord_dict_answerrs = OrderedDict(dict_answerrs)
        return ([x for x in ord_dict_answerrs][:2])

    def receive_poll_answer(self, update: Update, context: CallbackContext) -> None:
        """Summarize a users poll vote"""

        answer = update.poll_answer
        poll_id = answer.poll_id
        self.list_answer = list()
        try:
            questions = context.bot_data[poll_id]["questions"]
        # this means this poll answer update is from an old poll, we can't do our answering then
        except KeyError:
            return
        selected_options = answer.option_ids
        answer_string = ""
        for question_id in selected_options:
            self.list_answer.append(questions[question_id])
            if question_id != selected_options[-1]:
                answer_string += questions[question_id] + " and "
            else:
                answer_string += questions[question_id]

        context.bot.send_message(
                context.bot_data[poll_id]["chat_id"],
                f"{update.effective_user.mention_html()} выбрал {answer_string}!",
                parse_mode=ParseMode.HTML,
        )
        context.bot_data[poll_id]["answers"] += 1
        # Close poll after three participants voted
        if context.bot_data[poll_id]["answers"] == 20:
            self.list_cinema = ''.join([f'{x}\n' for x in self.cinema4watch(self.list_answer)])
            context.bot.send_message(
                    text=f'Опрос закрыт!, в след. среду({self.next_wednesday()}) смотрим:\n{self.list_cinema}',
                    chat_id=context.bot_data[poll_id]["chat_id"],
            )

            context.bot.unpin_chat_message(
                    chat_id=context.bot_data[poll_id]["chat_id"],
                    message_id=context.bot_data[poll_id]["message_id"]
            )

            context.bot.stop_poll(
                    context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
            )
            self.cinema.next_view(self.next_wednesday(), self.list_answer)

    @chk_user
    @log_error
    def create_poll_income(self, update: Update, context: CallbackContext):
        user_role = self.users.chk_role_user(update.effective_user.username)
        if user_role:
            context.bot.send_message(
                    text=f'{update.effective_user.mention_html()}, ты челядь, негоже тебе опросы создавать',
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
            )
            return ConversationHandler.END

        questions = ["Да, я буду", "Да буду я скорее всего", "Нет, меня не будет"]
        message = context.bot.send_poll(
                update.effective_chat.id,
                f"Кого ждать в среду({self.next_wednesday()})?",
                questions,
                is_anonymous=False,
                allows_multiple_answers=False,
                # open_period=30,
                close_date=self.next_wednesday(),
        )
        payload = {
            message.poll.id: {
                "questions": questions,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0,
            }
        }
        context.bot_data.update(payload)
        # Save some info about the poll the bot_data for later use in receive_poll_answer
        context.bot.pin_chat_message(
                chat_id=update.effective_chat.id,
                message_id=message.message_id,
        )

    @log_error
    def all_message(self, update: Update, context: CallbackContext):
        """Обработка всех входящих сообщений."""

        messages_text = {
            "ахмат сила": {"sticker": ["CAACAgIAAxkBAAICLGDBE8fnRHep4kxsPSEV-axEt8J4AAJPAAPXHi0GeLCyeFoYqwUfBA",
                                       "CAACAgIAAxkBAAICI2DBEs8OWKmi_s5V2vkk_tGz6bKHAAJNAAPXHi0Gyz6QUMa2fbIfBA"]},
            "шайтан": {"sticker": ["CAACAgIAAxkBAAIBKmC_M1CYl7JrWpXZT41F0MG4tyz0AALMAgAC1x4tBml4DooBSSkHHwQ"]},
            "путин": {"sticker": ["CAACAgIAAxkBAAECamBgw6PTDgUrOLUCMFxjhoci2VbNYwACJAYAAoA_ByhfcEf4inW0mx8E"]},
            " да ": {"sticker": ["CAACAgIAAxkBAAEDBw5hXYZkNILo7WOmHG9XwWflKrRF-QAC8A4AAj9UOEmedvYE79OfKCEE"]},
            " да.": {"sticker": ["CAACAgIAAxkBAAEDBw5hXYZkNILo7WOmHG9XwWflKrRF-QAC8A4AAj9UOEmedvYE79OfKCEE"]},
            "да": {"sticker": ["CAACAgIAAxkBAAEDBw5hXYZkNILo7WOmHG9XwWflKrRF-QAC8A4AAj9UOEmedvYE79OfKCEE"]}
        }

        for msg in messages_text.keys():
            logging.debug(f"Уфф, да тут словечко попалось {msg}")
            if msg in update.message.text.lower():
                context.bot.send_sticker(
                        chat_id=update.effective_chat.id,
                        sticker=choice(messages_text[msg]["sticker"])
                )

        if update.message.reply_to_message:
            if "послать" in update.message.text.lower():
                from_user = update.message.from_user.name
                to_user = update.message.reply_to_message.from_user.name
                if to_user == "@alco_cinema_club_bot":
                    msg_text = f'{from_user} - ты че собака сутулая? Тикай с городу'
                    context.bot.send_sticker(
                            chat_id=update.effective_chat.id,
                            sticker="CAACAgIAAxkBAAIBKmC_M1CYl7JrWpXZT41F0MG4tyz0AALMAgAC1x4tBml4DooBSSkHHwQ"
                    )
                else:
                    msg_text = f'Вы не поверите!! Но {from_user} послал нахуй {to_user}'
                context.bot.send_message(
                        text=msg_text,
                        chat_id=update.effective_chat.id
                )

    @chk_user
    @log_error
    def view_statistics(self, update: Update, context: CallbackContext):
        """
        /statistic (m) (y)
        m - номер месяца(по умолчанию текущий)
        y - год(по умолчанию текущий)

        -all год(по умолчанию текущий)

        Примеры:
            /statistic -all: -> month:False, year:False
            /statistic -m 7: -> month:Error, year:Хуйня, какая-то
            /statistic -y 2020: -> month:Error, year:Нет блять такого месяца, говно
            /statistic -m 4 -y 2020: -> month:4, year:2020
            /statistic -m 4 -y л: -> month:Error, year:Хуйня, какая-то
        """

        month, year = self.stat_com_prepare_params(update.message.text)

        if month == 'Error':
            update.message.reply_text(
                    text=year
            )

        text_to_message = self.cinema.for_statistic(month, year)

        if isinstance(text_to_message, str):
            update.message.reply_text(
                    text=text_to_message
            )
        else:
            text = self.prepare_stat_text(text_to_message)

            context.bot.send_message(
                    text=text,
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
            )

    @log_error
    def main(self):
        req = Request(
                connect_timeout=0.5,
                read_timeout=1.0,
        )
        bot = Bot(
                token=self.tg_token, request=req
        )
        updater = Updater(
                bot=bot,
                use_context=True,
        )

        # Проверить что бот корректно подключился к Telegram API
        logging.info(bot.get_me())

        # Навесить обработчики команд
        add_movie_handler = ConversationHandler(
                entry_points=[
                    CommandHandler('add', self.add_handler, pass_user_data=True),
                ],
                states={
                    FIND_MOVIE: [
                        MessageHandler(Filters.all, self.find_movie_handler, pass_user_data=True),
                    ],
                    FIND_DONE: [
                        CallbackQueryHandler(self.find_done_handler, pass_user_data=True),
                    ],
                    FINNALY_DONE: [
                        CallbackQueryHandler(self.finally_find_done, pass_user_data=True),
                    ],
                },
                fallbacks=[
                    CommandHandler('cancel', self.cancel_handler),
                ],
        )

        viewlist_movie_handler = ConversationHandler(
                entry_points=[
                    # CallbackQueryHandler(self.start_handler, pass_user_data=True),
                    CommandHandler('viewlist', self.viewlist_handler, pass_user_data=True),
                ],
                states={
                    NEXT: [
                        CallbackQueryHandler(self.viewlist_next_handler, pass_user_data=True),
                    ],
                    DETAIL_VIEW: [
                        CallbackQueryHandler(self.viewlist_detail_handler, pass_user_data=True),
                    ],
                    FINAL_VIEW: [
                        CallbackQueryHandler(self.viewlist_filnal_handler, pass_user_data=True),
                    ],
                },
                fallbacks=[
                    CommandHandler('cancel', self.cancel_handler),
                ],
        )

        updater.dispatcher.add_handler(add_movie_handler)
        updater.dispatcher.add_handler(viewlist_movie_handler)
        updater.dispatcher.add_handler(CommandHandler('create_poll', self.create_poll_handler))
        updater.dispatcher.add_handler(CommandHandler('who_income', self.create_poll_income))
        updater.dispatcher.add_handler(PollAnswerHandler(self.receive_poll_answer))
        updater.dispatcher.add_handler(CommandHandler('start', self.start_handler))
        updater.dispatcher.add_handler(CommandHandler('help', self.help_handler))
        updater.dispatcher.add_handler(CommandHandler('statistic', self.view_statistics))
        updater.dispatcher.add_handler(CommandHandler('normalno', self.normalno_handler))
        updater.dispatcher.add_handler(CommandHandler('rus_rulet', self.rus_rulet_handler))
        updater.dispatcher.add_handler(CommandHandler('get_rep_fys', self.get_rep_fys_handler))
        updater.dispatcher.add_handler(CommandHandler('insert_phrase', self.insert_main_phrase_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.all_message))

        # Начать бесконечную обработку входящих сообщений
        try:
            updater.start_polling()
            updater.idle()
        except:
            pass


if __name__ == '__main__':
    logging.info('Start bot')
    AlcoCinemaBot().main()
