# -*- coding: utf-8 -*-
import logging
from datetime import date, timedelta

from .config import *
import psycopg2

# Логирование
logging.basicConfig(filename="acc_bot.log", level=logging.INFO, format='%(levelname)s %(filename)s %(module)s.%(funcName)s | %(asctime)s: %(message)s', )

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

	def nextWednesday(self):
		tdelta = timedelta(7)
		td = date.today()
		beforeStr = (td+timedelta(3-td.isoweekday()) + tdelta)
		return date.strftime(beforeStr, '%d.%m.%Y')

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



if __name__ == '__main__':
	BotSetting().pg_connect()
