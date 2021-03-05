# -*- coding: utf-8 -*-
import logging

from kinopoisk.movie import Movie

from .bot_setting import BotSetting, logging

class Cinema(BotSetting):
	def __init__(self):
		BotSetting.__init__(self)


	def find_cinema(self, cinema_title):
		movies = Movie.objects.search(f'{cinema_title}')
		list_movies = list()

		for id, movie in enumerate(movies):
			movie.title_en = movie.title_en.replace("'", "`")
			tmp_dict = {u'id': id,
						u'title': movie.title,
						u'year': movie.year if movie.year else 'null',
						u'title_en': f"'{movie.title_en}'" if movie.title_en else 'null',
						u'runtime': movie.runtime if movie.runtime else 'null',
						u'rating': movie.rating if movie.rating else 'null'
						}
			list_movies.append(tmp_dict)
		return list_movies

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
                            {cinema_dict['year']},
                            {cinema_dict['title_en']},
                            {cinema_dict['runtime']},
                            {cinema_dict['rating']},
                            {cinema_dict['user_pk']},
							{is_watch}
                            )
						ON CONFLICT (title, movie_year, title_en) DO UPDATE SET watch_status = {is_watch}
                    """
			try:
				self.cursor.execute(sql)
				self.conn.commit()
			except Exception as e:
				self.cursor.execute('END TRANSACTION;')
				logging.error(f'{e}\n{sql}')
				return False

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

	def for_statistic(self, month, year):
		param_month = f"and EXTRACT(month FROM c.watch_date) = {month}" if month else ""
		param_year = f"and EXTRACT(year FROM c.watch_date) = {year}" if year else ""
		sql = f"""SELECT * FROM public.cinema c WHERE watch_status = true
				 {param_year} {param_month}"""
		self.cursor.execute(sql)
		keys = [x.name for x in self.cursor.description]
		if self.cursor:
			statis_dict = [dict(zip(keys, x)) for x in self.cursor.fetchall()]
		else:
			statis_dict = f'Бля, кажись нет данных за {month} месяц {year} года'
		return statis_dict

	def next_view(self, day, list_movie):
		for movie in list_movie:
			movie = movie.split("(")[0].strip()
			sql = f"UPDATE cinema SET watch_date = '{day}' where title = '{movie}'"
			self.cursor.execute(sql.format(movie))
		self.conn.commit()


if __name__ == '__main__':
	Cinema()
