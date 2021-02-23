# -*- coding: utf-8 -*-

from kinopoisk.movie import Movie

from .bot_setting import BotSetting


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

	def insert_cinema(self, cinema_dict: None):
		sql_chk = f"""SELECT * FROM cinema
						where title = '{cinema_dict['title']}' and
						title_en = '{cinema_dict['title_en']}' and
						movie_year = '{cinema_dict['year']}'"""
		self.cursor.execute(sql_chk)
		if self.cursor.fetchone():
			return False

		if cinema_dict:
			sql = f"""insert into cinema(title, movie_year, title_en, runtime, rating, added)
						values(
							'{cinema_dict['title']}',
							'{cinema_dict['year']}',
							'{cinema_dict['title_en']}',
							{cinema_dict['runtime']},
							{cinema_dict['rating']},
							{cinema_dict['user_pk']}
							)
					"""
			self.cursor.execute(sql)
			self.conn.commit()
		return True

	def view_list(self):
		sql = u"""select c.title, c.movie_year, c.rating from cinema c
				where c.watch_status = 0;"""
		self.cursor.execute(sql)
		keys = [x.name for x in self.cursor.description]
		return [dict(zip(keys, x)) for x in self.cursor.fetchall()]


if __name__ == '__main__':
	Cinema()
