from fastapi import HTTPException
from starlette import status


class UserAlreadyRegisterIntoThisChat(HTTPException):
    """
    Исключение, выбрасываемое, когда пользователь уже зарегистрирован в данном чате.

    Используется для предотвращения повторной регистрации одного и того же пользователя
    в одном чате. Статус 409 Conflict указывает на конфликт текущего запроса с состоянием сервера.
    """

    def __init__(self, detail: str = "Ты дурак? ты уже регистрировался в данном чате"):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserIsNotRegisteredIntoThisChat(HTTPException):
    """
    Исключение, выбрасываемое, когда пользователь не зарегистрирован в данном чате.

    Используется для блокировки доступа к функционалу рулетки пользователям, которые
    не прошли регистрацию.
    """

    def __init__(
        self, detail: str = "Ты не зарегистрировался, значит не участвуешь в рулетке."
    ):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)
