# -*- coding: utf-8 -*-

"""Настройки бота"""

import logging
from datetime import date, timedelta, datetime
from random import randint

import psycopg2
from prettytable import from_db_cursor

from .config import tg_token, pg_connect

# Логирование
logging.basicConfig(filename="acc_bot.log", level=logging.INFO,
                    format='%(levelname)s %(filename)s %(module)s.%(funcName)s | %(asctime)s: %(message)s', )


def log_error(func):
    """
    декортатор логирования
    :param func: функция
    :return:
    """

    def inner(*args, **kwargs):
        """
        внутренняя функция декоратора логирования
        """
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print(f'{func.__name__}: {error}'.encode('utf8'))
            logging.error(f'{func.__name__}: {error}'.encode('utf8'))

    return inner


@log_error
def chk_user(func):
    """
    Декоратор для проверки есть ли пользователь в БД
    """

    def inner(*args, **kwargs):
        """
        Проверка пользователя и запись в лог его действия
        :param args:
        :param kwargs:
        :return:
        """
        if args[1].update_id:
            user = args[1].message.from_user.username
            first_name = args[1].message.from_user.first_name
            full_name = args[1].message.from_user.full_name
            chat_id = args[1].message.from_user.id
            w_user = WorkWithUser()
            w_user.chk_users(user, first_name, full_name)
            if '/' in args[1].message.text:
                logging.info(f'Пользователь: {user}, Запустил комаду: {args[1].message.text}, chat_id: {chat_id}')
        return func(*args, **kwargs)

    return inner


class BotSetting:
    """
    Дополнительный класс для работы бота
    """

    def __init__(self):
        self.conn, self.cursor = self.pg_connect()
        self.tg_token = tg_token

    @staticmethod
    def pg_connect():
        """
        Подключение к pg
        """
        conn = psycopg2.connect(dbname=pg_connect['dbname'],
                                user=pg_connect['user'],
                                password=pg_connect['password'],
                                host=pg_connect['host'],
                                port=pg_connect['port'])

        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def next_closest(search_day):
        """
        Расчитать дату дня следующей неделт
        :param search_day: день недели, дату которогонадо найти на след. неделе
        :return: дата
        """
        today = date.today()
        from_day = today.isoweekday()
        different_days = search_day - from_day if from_day < search_day else 7 - from_day + search_day
        return today + timedelta(days=different_days)

    def next_monday(self):
        """
        След. понедельник
        :return: дата
        """
        return date.strftime(self.next_closest(1), '%d.%m.%Y')

    def next_tuesday(self):
        """
        След. вторник
        :return: дата
        """
        return date.strftime(self.next_closest(2), '%d.%m.%Y')

    def next_wednesday(self):
        """
        След. среда
        :return: дата
        """
        return date.strftime(self.next_closest(3), '%d.%m.%Y')

    def next_thursday(self):
        """
        След. четверг
        :return: дата
        """
        return date.strftime(self.next_closest(4), '%d.%m.%Y')

    def next_friday(self):
        """
        След. пятница
        :return: дата
        """
        return date.strftime(self.next_closest(5), '%d.%m.%Y')

    def stat_com_prepare_params(self, command_text):
        """
        подготовка параметров для команды статистики
        :param command_text: команда
        :return: тест статистики
        """

        needs_month, needs_year = None, None
        command_text = command_text.split(" ")[1:]
        commands = dict(zip(command_text[::2], command_text[1::2]))

        if '@' in command_text:
            command_text = command_text.split('@')[0]

        elif '-all' in command_text:
            needs_month, needs_year = False, False

        elif commands.get('-y'):
            month = commands.get('-m') if commands.get('-m') else False
            year = commands.get('-y')
            if month and month not in [f'{x}' for x in range(1, 13)]:
                needs_month, needs_year = 'Error', 'Нет блять такого месяца, говно'
            elif year not in [f'{x}' for x in range(2018, 2033)]:
                needs_month, needs_year = 'Error', 'Ну и что ты ввел? ишак'
            needs_month, needs_year = month, year
        elif commands.get('-m'):
            year = commands.get('-y') if commands.get('-y') else datetime.today().year
            month = commands.get('-m')
            year_range = [x for x in range(1970, 2033)]
            month_range = [f'{x}' for x in range(1, 13)]
            if month not in month_range:
                needs_month, needs_year = 'Error', 'Нет блять такого месяца, говно'
            elif year not in year_range:
                needs_month, needs_year = 'Error', 'Ну и что ты ввел? ишак'
            needs_month, needs_year = month, year

        elif command_text == [] or command_text == '/statistic':
            needs_month, needs_year = date.today().month, date.today().year

        else:
            text_help = """
                Примеры:
                /statistic -all: за все время
                /statistic -m 7: 7 месяц этого года
                /statistic -y 2020: За весь 2020 год
                /statistic -m 4 -y 2020: за 4 месяц 2020 года
                /statistic -m 4 -y л: ошибка"""
            needs_month, needs_year = 'Error', f'Хуйня ты ебаная, не правильно кулючи заюзал, {text_help}'
        return needs_month, needs_year

    def prepare_stat_text(self, dict_movies):
        """
        Подготовка текста для вывода статистики
        :param dict_movies: словарь фильмов
        :return: тест для отправки в бот
        """
        cinema_list = '\n'.join([x['title'] for x in dict_movies])
        count_movies = len(dict_movies)
        count_min = sum([x['runtime'] if x['runtime'] else 0 for x in dict_movies])
        count_hours = f"{count_min // 60} час(а/ов) {count_min % 60} мин."
        text = f"""
                Ну`с итого:\n{cinema_list}
                -------------
                В сумме на просмотр мы потратили: {count_hours}
                и посмотрели: {count_movies} фильма
                """
        return text

    def insert_main_phrase(self, text):
        """
        Добавление фразы для русской рулетки
        :param text: Текст с обязательным наличием @
         для указания в какое место необходимо вставить логин

        """
        text = text.replace('@', '@{user}')
        query_insert = f"""INSERT INTO public.main_words
                        (words)
                        VALUES('{text}')"""
        try:
            self.cursor.execute(query_insert)
            self.conn.commit()
            return True
        except:
            return False


class WorkWithUser(BotSetting):
    """
    Класс для работы с пользователями
    """

    def __init__(self):
        BotSetting.__init__(self)

    def chk_users(self, username, first_name=None, full_name=None):
        """
        Проверка наличия пользователя в БД,
        если отсутствует добавляется.
        :param username: username пользователя
        :param first_name: Если в тг указано основное имя
        :param full_name: Если в тг указано полное имя
        :return: id пользователя
        """
        sql = f"SELECT id from users where username = '{username}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        if not result:
            result = self.add_user(username, first_name, full_name)
        return result[0]

    def add_user(self, username, first_name, full_name):
        """

        :param username: параметр из tg
        :param first_name: параметр из tg
        :param full_name: параметр из tg
        :return: id пользователя
        """
        sql = f"""INSERT INTO users(username, first_name, full_name)
                    VALUES('{username}','{first_name}', '{full_name}') RETURNING id"""
        self.cursor.execute(sql)
        self.conn.commit()
        logging.info(f'В БД добавлен пользователь под ником "{username}"')
        return self.cursor.fetchone()

    def chk_role_user(self, username):
        """
        Проверка ролей пользователя
        :param username: параметр из tg
        :return: bool
        """
        sql = f"""SELECT u.username, r.role_name
                    FROM users u 
                    JOIN roles r on r.id = u.role 
                    WHERE u.username = '{username}' 
                        AND r.role_name = 'user'"""
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return True if result else False

    def get_all_users(self):
        """
        Вывевсти всех пользоавтелей
        :return: список пользователей
        """
        sql = "SELECT id, username FROM public.users"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def calc_goes_fuck_to_self(self, user_id):
        """
        Записать в БД кого послали нахуй, че тут еще писать-то?
        :param user_id: id пользоавтеля из БД
        """
        sql = f"INSERT INTO public.fuck_your_selfs (user_id) VALUES({user_id})"
        self.cursor.execute(sql)
        self.conn.commit()

    def get_report_fys(self):
        """
        Формирвоание статистики кого сколько раз послали нахуй
        :return: текст статисттики
        """
        sql = u"""SELECT u.username, count(fys.id)
                    FROM public.users u
                    LEFT JOIN public.fuck_your_selfs fys on fys.user_id = u.id
                    GROUP BY u.username 
                    ORDER BY count(fys.id) desc;"""
        self.cursor.execute(sql)
        mytable = from_db_cursor(self.cursor)
        text = f"<code>Количество посыланий нахуй:\n{mytable}</code>"
        return text

    def get_user_for_rulet(self):
        """
        Выбрать пользоавтеля который сейчас будет послан нахуй
        :return: Пользователь
        """
        users = self.get_all_users()
        index_random_user = randint(0, len(users) - 1)
        user = users[index_random_user]
        return user

    def get_main_word(self):
        """
        Выбрать фразу которой пользователь будет послан нахуй
        :return: фраза из БД
        """
        sql = u"""SELECT words from public.main_words"""
        self.cursor.execute(sql)
        main_words = self.cursor.fetchall()
        index_main_words = randint(0, len(main_words) - 1)
        main_word = main_words[index_main_words]
        return f'{main_word[0]}\n'


if __name__ == '__main__':
    BotSetting().pg_connect()
