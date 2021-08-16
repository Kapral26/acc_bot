import unittest

from main_bot.setting.cinema import Cinema


class TestCinema(unittest.TestCase, Cinema):
    def setUp(self):
        Cinema.__init__(self)
        self.test_cinema = {'id': 0,
                            "title": "La Toya Jackson: Heart Don't Lie (видео)",
                            'year': 1984,
                            'title_en': 'null',
                            'runtime': 3,
                            'rating': 'null'}

    def test_find_cinema(self):
        title_cinema = "La Toya Jackson: Heart Don't Lie"

        list_movies = self.find_cinema(title_cinema)
        self.assertEqual(self.test_cinema, list_movies[0], "Шото не тот фильм был найден")

    def test_insert_cinema(self):
        test_insert_cinema = {'id': 0,
                            "title": "test_cinema",
                            'year': 1984,
                            'title_en': 'test_cinema',
                            'runtime': 3,
                            'rating': 'null',
                            "user_pk": 1}
        result_insert = self.insert_cinema(test_insert_cinema)
        self.assertTrue(result_insert, "А фильм то не добавился в БД")

        # Попытка второго инсерта фильма
        result_availability = self.chk_availability(test_insert_cinema)
        self.assertTrue(result_availability)

    def test_movie_detail(self):
        movie_datail_equal = ["Название: 'test_cinema'",
                              "В оригинале: 'test_cinema'",
                              'Продолжительность: 0 час(а/ов) 3 мин.',
                              'Рейтинг: None']
        movie_datail_equal = "\n".join(movie_datail_equal)

        movie_id = self._pg_execute(f"select id from cinema where title = 'test_cinema';").fetchone()[0]
        movie_detail = self.movie_detail(movie_id)

        self.assertEqual(movie_detail, movie_datail_equal, "Описание фильма то не совпадает")

    def tearDown(self):
        sql = f"DELETE FROM cinema where title = 'test_cinema';"
        self._pg_execute(sql)


if __name__ == '__main__':
    unittest.main()
