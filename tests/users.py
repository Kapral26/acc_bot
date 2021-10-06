import unittest

from main_bot.setting.bot_setting import PgConnect, WorkWithUser


class TestUser(unittest.TestCase, PgConnect):

    def setUp(self) -> None:
        PgConnect.__init__(self)
        self.users = WorkWithUser()

    def test_add_user(self):
        # Простой пользователль
        test_username = "test_user"
        test_first_name = "testuser"
        test_full_name = "testuser"

        # Пользователь админ
        admin_username = "test_admin"
        admin_first_name = "test_admin"
        admin_full_name = "test_admin"
        admin_role = 3

        test_user_id = self.users.add_user(test_username, test_first_name, test_full_name)
        admin_user_id = self.users.add_user(admin_username, admin_first_name, admin_full_name, admin_role)

        self.assertIsInstance(test_user_id, tuple, "Проблема с добавлением пользоавтеля test_user")
        self.assertIsInstance(admin_user_id, tuple, "Проблема с добавлением пользоавтеля test_admin")

    def test_chk_users(self):
        test_username = "test_user"
        admin_username = "test_admin"

        test_user_id = self.users.chk_users(test_username)
        admin_user_id = self.users.chk_users(admin_username)

        self.assertIsInstance(test_user_id, tuple, "Проблема с проверкой пользователя test_user")
        self.assertIsInstance(admin_user_id, tuple, "Проблема с проверкой пользователя admin_user")

    def test_chk_roles(self):
        test_username = "test_user"
        admin_username = "test_admin"
        test_user_chk_role_res = self.users.chk_role_user(test_username)
        admin_user_chk_role_res = self.users.chk_role_user(admin_username)

        self.assertTrue(test_user_chk_role_res, "Проверка роли user У пользователя не прошла")
        self.assertFalse(admin_user_chk_role_res, "Проверка роли user У пользователя не прошла")

    def tearDown(self) -> None:
        sql = """
            DELETE FROM users u
            WHERE u.username IN ('test_user', 'test_admin')"""
        self._pg_execute(sql, commit=True)



if __name__ == '__main__':
    unittest.main()
