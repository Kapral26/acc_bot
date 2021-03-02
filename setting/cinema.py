# -*- coding: utf-8 -*-
import logging

from kinopoisk.movie import Movie

from .bot_setting import BotSetting, logging

class Cinema(BotSetting):
	def __init__(self):
		BotSetting.__init__(self)
		self.list_movies = list()

	def find_cinema(self, cinema_title):
		movies = Movie.objects.search(f'{cinema_title}')

		for id, movie in enumerate(movies):
			tmp_dict = {u'id': id,
						u'title': movie.title,
						u'year': movie.year,
						u'title_en': movie.title_en.replace("'", "`"),
						u'runtime': movie.runtime,
						u'rating': movie.rating}
			self.list_movies.append(tmp_dict)
		return self.list_movies

	def insert_cinema(self, cinema_dict: None, is_watch=False):
		sql_chk = f"""SELECT * FROM cinema
                        where title = '{cinema_dict['title']}' and
                        title_en = '{cinema_dict['title_en']}' and
                        movie_year = '{cinema_dict['year']}'"""
		try:
			self.cursor.execute(sql_chk)
			if self.cursor.fetchone():
				return False
		except:
			self.cursor.execute('END TRANSACTION;')

		if cinema_dict:
			sql = f"""insert into cinema(title, movie_year, title_en, runtime, rating, added, watch_status)
                        values(
                            '{cinema_dict['title']}',
                            '{cinema_dict['year']}',
                            '{cinema_dict['title_en']}',
                            {cinema_dict['runtime']},
                            {cinema_dict['rating']},
                            {cinema_dict['user_pk']},
							{is_watch}
                            )
                    """
			try:
				self.cursor.execute(sql)
				self.conn.commit()
			except Exception as e:
				self.cursor.execute('END TRANSACTION;')
				logging.error(f'{e}\n{sql}')

		return True

	def view_list(self):
		sql = u"""select c.title, c.movie_year, c.id from cinema c
                where c.watch_status = false;"""
		self.cursor.execute(sql)
		keys = [x.name for x in self.cursor.description]
		return [dict(zip(keys, x)) for x in self.cursor.fetchall()]

	def movie_detail(self, id):
		sql = f"SELECT title, movie_year, title_en, runtime, rating FROM public.cinema where id = {id}"
		self.cursor.execute(sql)
		keys = [x.name for x in self.cursor.description]
		movie_dict = [dict(zip(keys, x)) for x in self.cursor.fetchall()][0]
		movie_dict['runtime'] = f"{movie_dict['runtime'] // 60} час(а\ов) {movie_dict['runtime'] % 60} мин."
		detail_text = [f"Название: '{movie_dict['title']}'",
					   f"В оригинале: '{movie_dict['title_en']}'",
					   f"Продолжительность: {movie_dict['runtime']}",
					   f"Рейтинг: {movie_dict['rating']}"]

		return '\n'.join(detail_text)

	def mark_viewed(self, id):
		sql = f'UPDATE cinema set watch_status = true, poll = false, watch_date = current_date where id = {id}'
		self.cursor.execute(sql)
		self.conn.commit()
		return "Я понял, посмотрели фильм. Че выёбываешься?"

	def to_poll(self, id):
		sql = f'UPDATE cinema set poll = true where id = {id}'
		self.cursor.execute(sql)
		self.conn.commit()
		return "Фильм будет в след. опросе"

	def for_create_poll(self):
		sql = 'select c.title, c.movie_year from cinema c where c.poll is true '
		self.cursor.execute(sql)
		return [f'{x} ({y})' for x, y in self.cursor.fetchall()]


if __name__ == '__main__':
	Cinema()
