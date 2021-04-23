# -*- coding: utf-8 -*-
import logging
from datetime import date, timedelta, datetime

import psycopg2
from prettytable import PrettyTable, from_db_cursor

from .config import *

# Логирование
logging.basicConfig(filename="acc_bot.log", level=logging.INFO,
					format='%(levelname)s %(filename)s %(module)s.%(funcName)s | %(asctime)s: %(message)s', )


def log_error(f):
	def inner(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except Exception as e:
			print(f'{f.__name__}: {e}'.encode('utf8'))
			logging.error(f'{f.__name__}: {e}'.encode('utf8'))

	return inner


@log_error
def chk_user(f):
	def inner(*args, **kwargs):
		if args[1].update_id:
			user = args[1].message.from_user.username
			first_name = args[1].message.from_user.first_name
			full_name = args[1].message.from_user.full_name
			chat_id = args[1].message.from_user.id
			wUser = workWithUser()
			wUser.chk_users(user, first_name, full_name)
			if '/' in args[1].message.text:
				logging.info(f'Пользователь: {user}, Запустил комаду: {args[1].message.text}, chat_id: {chat_id}')
		return f(*args, **kwargs)

	return inner


class BotSetting:
	def __init__(self):
		self.pg_connect()
		self.tg_token = tg_token

	def pg_connect(self):
		self.conn = psycopg2.connect(dbname=pg_connect['dbname'], user=pg_connect['user'],
									 password=pg_connect['password'], host=pg_connect['host'])
		self.cursor = self.conn.cursor()

	def next_closest(self, search_day):
		td = date.today()
		from_day = td.isoweekday()
		different_days = search_day - from_day if from_day < search_day else 7 - from_day + search_day
		return td + timedelta(days=different_days)



	def nextMonday(self):
		return date.strftime(self.next_closest(1), '%d.%m.%Y')

	def nextTuesday(self):
		return date.strftime(self.next_closest(2), '%d.%m.%Y')

	def nextWednesday(self):
		return date.strftime(self.next_closest(3), '%d.%m.%Y')

	def nextThursday(self):
		return date.strftime(self.next_closest(4), '%d.%m.%Y')


	def nextFriday(self):
		return date.strftime(self.next_closest(5), '%d.%m.%Y')

	def prepare_params(self, command_text):
		if '@' in command_text:
			command_text = command_text.split('@')[0]

		if '/statistic' == command_text:
			return date.today().month, date.today().year

		command_text = command_text.split(" ")[1:]
		commands = dict(zip(command_text[::2], command_text[1::2]))

		if '-all' in command_text:
			return False, False
		elif commands.get('-y'):
			m = commands.get('-m') if commands.get('-m') else False
			y = commands.get('-y')
			if m and m not in [f'{x}' for x in range(1,13)]:
				return 'Error', 'Нет блять такого месяца, говно'
			elif y not in [f'{x}' for x in range(2018, 2033)]:
				return 'Error', 'Ну и что ты ввел? ишак'
			return m, y
		elif commands.get('-m'):
			y = commands.get('-y') if commands.get('-y') else datetime.today().year
			m = commands.get('-m')
			if m not in [f'{x}' for x in range(1,13)]:
				return 'Error', 'Нет блять такого месяца, говно'
			elif y not in [x for x in range(1970, 2033)]:
				return 'Error', 'Ну и что ты ввел? ишак'
			return m, y
		else:
			text_help = """
				Примеры:
				/statistic -all: за все время
				/statistic -m 7: 7 месяц этого года
				/statistic -y 2020: За весь 2020 год
				/statistic -m 4 -y 2020: за 4 месяц 2020 года
				/statistic -m 4 -y л: ошибка"""
			return 'Error', f'Хуйня ты ебаная, не правильно кулючи заюзал, {text_help}'

	def prepare_stat_text(self, dict_movies):
		cinema_list = '\n'.join([x['title'] for x in dict_movies])
		count_movies = len(dict_movies)
		count_min = sum([x['runtime'] for x in dict_movies])
		count_hours = f"{count_min // 60} час(а\ов) {count_min % 60} мин."
		text = f"""
				Ну`с итого:\n{cinema_list}
				-------------
				В сумме на просмотр мы потратили: {count_hours}
				и посмотрели: {count_movies} фильма
				"""
		return text

class workWithUser(BotSetting):
	def __init__(self):
		BotSetting.__init__(self)

	def chk_users(self, user, first_name=None, full_name=None):
		sql = f"SELECT id from users where username = '{user}'"
		self.cursor.execute(sql)
		result = self.cursor.fetchone()

		if not result:
			result = self.add_user(user, first_name, full_name)
		return result[0]

	def add_user(self, user, first_name, full_name):
		sql = f"insert into users(username, first_name, full_name) values('{user}','{first_name}', '{full_name}') RETURNING id"
		self.cursor.execute(sql)
		self.conn.commit()
		logging.info(f'В БД добавлен пользователь под ником "{user}"')
		return self.cursor.fetchone()

	def its_user(self, user):
		sql = f"select u.username, r.role_name from users u join roles r on r.id = u.role where u.username = '{user}' and r.role_name = 'user'"
		self.cursor.execute(sql)
		result = self.cursor.fetchone()
		return True if result else False

	def get_all_users(self):
		sql = "SELECT id, username FROM public.users"
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		return result

	def calc_goes_fuck_to_self(self, user_id):
		sql = f"INSERT INTO public.fuck_your_selfs (user_id) VALUES({user_id})"
		self.cursor.execute(sql)
		self.conn.commit()

	def get_report_fys(self):

		sql = u"""SELECT u.username, count(fys.id) FROM public.users u
					left join public.fuck_your_selfs fys on fys.user_id = u.id
					group by u.username 
					order by count(fys.id) desc;"""
		self.cursor.execute(sql)
		mytable = from_db_cursor(self.cursor)
		text = f"<code>Количество посыланий нахуй:\n{mytable}</code>"
		return text


if __name__ == '__main__':
	BotSetting().pg_connect()
