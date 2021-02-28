# -*- coding: utf-8 -*-

from collections import Counter, OrderedDict

from setting.bot_setting import BotSetting, workWithUser, log_error, logging, chk_user
from setting.cinema import Cinema
from telebot.apihelper import get_chat_members_count
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater, MessageHandler, CommandHandler, \
	ConversationHandler, Filters, PollAnswerHandler
from telegram.utils.request import Request

FIND_MOVIE, FIND_DONE = range(2)
NEXT, DETAIL_VIEW, VIEW_ALL, FINAL_VIEW = range(4)

CALLBACK_BEGIN = 'x1'


class newVersionBot(BotSetting):
	def __init__(self):
		BotSetting.__init__(self)
		self.cinema = Cinema()
		self.users = workWithUser()

	@chk_user
	@log_error
	def help_handler(self, update: Update, context: CallbackContext):
		""" Не относится к сценарию диалога, но создаёт начальные inline-кнопки
        """

		update.message.reply_text(
				'Cписок команд:\n'
				'/help выведет тебе все необходимые команды\n'
				'/add добавить фильм в лист ожидания\n'
				'/viewlist - Вывести фильмы из листа ожидания\n'
				'/normalno\n'
				'/dowatch - Вывести 2 фильма из списка\n'
				'/iswatch - Отметить фильм, как просмотренный\n',
				parse_mode=ParseMode.HTML,
		)

	@chk_user
	@log_error
	def start_handler(self, update: Update, context: CallbackContext):
		""" Не относится к сценарию диалога, но создаёт начальные inline-кнопки
        """
		self.count_users = get_chat_members_count(
				token=self.tg_token,
				chat_id=update.message.chat_id,
		)

		update.message.reply_text(
				f'Бот АлкоКиноКлуба\nКоличество участников: {self.count_users}\n'
				'Не забудь пройти по направлению\n'
				'Чтобы посмотреть список команд:\n'
				'/help',
				parse_mode=ParseMode.HTML,
		)

	@chk_user
	@log_error
	def normalno_handler(self, update: Update, context: CallbackContext):
		update.message.reply_text(
				f'{update.effective_user.mention_html()}, Пошел на хуй!\n'
				'https://www.google.ru/maps/place/Nahui,+08270,+%D0%9F%D0%B5%D1%80%D1%83/@-14.4098416,-71.3077453,15z/data=!3m1!4b1!4m5!3m4!1s0x91692f289ed899f9:0x478a165988814b94!8m2!3d-14.4098412!4d-71.2989897',
				# parse_mode=ParseMode.MARKDOWN,
				disable_web_page_preview=False,
				parse_mode=ParseMode.HTML,
		)

	@chk_user
	@log_error
	# /add команда для добавления фильма в список
	def add_handler(self, update: Update, context: CallbackContext):
		""" Начало взаимодействия по клику на inline-кнопку
        """
		chat_id = update.message.chat_id

		update.message.bot.send_message(
				chat_id=chat_id,
				text='Введи название фильма:',
		)
		return FIND_MOVIE

	@log_error
	def find_movie_handler(self, update: Update, context: CallbackContext):

		if update.message.text == '/cancel':
			return ConversationHandler.END

		context.user_data[FIND_MOVIE] = update.message.text
		# logger.info('user_data: %s', context.user_data)

		self.movies = self.cinema.find_cinema(context.user_data[FIND_MOVIE])

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
				# text=f'Выбери id фильма, которые необходимо добавить \n {text}',
				reply_markup=inline_buttons,
		)
		return FIND_DONE

	@log_error
	def find_done_handler(self, update: Update, context: CallbackContext):

		if update.callback_query.data == 'cancel':
			context.bot.send_message(
					text='Отмена.\nЧтобы начать сначала введите: /add',
					chat_id=update.effective_chat.id
			)
			return ConversationHandler.END

		movie_id = int(update.callback_query.data)
		movie_data = [x for x in self.movies if x['id'] == movie_id][0]
		movie_data['user_pk'] = self.users.chk_users(user=update.effective_chat.username)
		context.user_data[FIND_DONE] = movie_data

		save_result = self.cinema.insert_cinema(movie_data)

		if save_result:
			text_done = f'''Все данные успешно сохранены!\nФильм: "{movie_data['title']}"\nдобавлен в список'''
		else:
			text_done = f'''Фильм: "{movie_data['title']}" ранее был добавлен'''

		# Завершить диалог
		update.effective_message.reply_text(
				text=text_done,

		)
		return ConversationHandler.END

	@log_error
	def cancel_handler(self, update: Update, context: CallbackContext):
		""" Отменить весь процесс диалога. Данные будут утеряны
        """
		update.message.reply_text('Отмена.\nЧтобы начать сначала введите: /add')
		return ConversationHandler.END

	@chk_user
	@log_error
	def viewlist_handler(self, update: Update, context: CallbackContext):
		self.dict_list_movie = self.cinema.view_list()
		count_view = 5  # 11

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
		callback_view = update.callback_query
		callback_view.answer()
		if callback_view.data == 'all':
			return VIEW_ALL

		if 'd;' in callback_view.data:
			context.user_data[DETAIL_VIEW] = int(callback_view.data.split(';')[1])
			return DETAIL_VIEW

		count_view = int(update.callback_query.data)
		count_view_next = count_view + 5  # 10

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
		user_role = self.users.its_user(update.effective_user.username)
		if user_role:
			context.bot.send_message(
					text=f'{update.effective_user.mention_html()}, ты челядь, негоже тебе опросы создавать',
					chat_id=update.effective_chat.id,
					parse_mode=ParseMode.HTML,
			)
			return ConversationHandler.END

		questions = self.cinema.for_create_poll()
		message = context.bot.send_poll(
				update.effective_chat.id,
				f"Псс, ребзи в среду({self.nextWednesday()}) собираемся,\nЧто будем смотреть?",
				questions,
				is_anonymous=False,
				allows_multiple_answers=True,
				# open_period=30,
				close_date=self.nextMonday(),
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

	def receive_poll_answer(self, update: Update, context: CallbackContext) -> None:
		"""Summarize a users poll vote"""

		def cinema4watch(list):
			dict_answerrs = Counter(list)
			ord_dict_answerrs = OrderedDict(dict_answerrs)
			return ([x for x in ord_dict_answerrs][:2])

		answer = update.poll_answer
		poll_id = answer.poll_id
		list_answer = list()
		try:
			questions = context.bot_data[poll_id]["questions"]
		# this means this poll answer update is from an old poll, we can't do our answering then
		except KeyError:
			return
		selected_options = answer.option_ids
		answer_string = ""
		for question_id in selected_options:
			list_answer.append(questions[question_id])
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
		if context.bot_data[poll_id]["answers"] == 5:
			list_cinema = ''.join([f'{x}\n' for x in cinema4watch(list_answer)])
			context.bot.send_message(
					text=f'Опрос закрыт!, в след. среду({self.nextWednesday()}) смотрим:\n{list_cinema}',
					chat_id=context.bot_data[poll_id]["chat_id"],
			),

			context.bot.unpin_all_chat_messages(
					chat_id=context.bot_data[poll_id]["chat_id"]
			)

			context.bot.stop_poll(
					context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
			)

	@log_error
	def main(self):
		req = Request(
				connect_timeout=0.5,
				read_timeout=1.0,
		)
		bot = Bot(
				token=self.tg_token,
				base_url='https://telegg.ru/orig/bot'
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
					# CallbackQueryHandler(self.start_handler, pass_user_data=True),
					CommandHandler('add', self.add_handler, pass_user_data=True),
				],
				states={
					FIND_MOVIE: [
						MessageHandler(Filters.all, self.find_movie_handler, pass_user_data=True),
					],
					FIND_DONE: [
						CallbackQueryHandler(self.find_done_handler, pass_user_data=True),
					]
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

		create_poll_handler = ConversationHandler(
				entry_points=[
					CommandHandler('create_poll', self.create_poll_handler, pass_user_data=True),
				],
				states={
					NEXT: [
						CallbackQueryHandler(self.viewlist_next_handler, pass_user_data=True),
					],
				},
				fallbacks=[
					CommandHandler('cancel', self.cancel_handler),
				],
		)

		updater.dispatcher.add_handler(add_movie_handler)
		updater.dispatcher.add_handler(viewlist_movie_handler)
		updater.dispatcher.add_handler(create_poll_handler)
		updater.dispatcher.add_handler(PollAnswerHandler(self.receive_poll_answer))
		updater.dispatcher.add_handler(CommandHandler('start', self.start_handler))
		updater.dispatcher.add_handler(CommandHandler('help', self.help_handler))
		updater.dispatcher.add_handler(CommandHandler('normalno', self.normalno_handler))

		# Начать бесконечную обработку входящих сообщений
		try:
			updater.start_polling()
			updater.idle()
		except:
			pass


if __name__ == '__main__':
	logging.info('Start bot')
	newVersionBot().main()
