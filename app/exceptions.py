class RoleNotFoundException(Exception):

    detail = "Roles not found"


class BadPhraseNotFoundError(Exception):

    detail = "Не найдена фраза для отправки по направлению. Вероятно они вовсе не добавлены."


