from fastapi import HTTPException
from starlette import status


class UserWasExits(Exception):
    detail = "User was exist"


class UserAlreadyRegisterIntoThisChat(HTTPException):
    def __init__(self, detail="Ты дурак? ты уже регистрировался в данном чате"):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserRoleHasAlreadyBeenEstablishedException(Exception):
    detail = "Role has already been established"


class UserRoleNotFount(Exception):
    detail = "User don`t has role in this chat"


class UserNotFoundError(Exception):
    detail = "User not found"
