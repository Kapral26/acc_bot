class UserWasExits(Exception):
    detail = "User not found"

class UserRoleHasAlreadyBeenEstablishedException(Exception):
    detail = "Role has already been established"


class UserRoleNotFount(Exception):
    detail = "User don`t has role in this chat"

class UserNotFoundError(Exception):


    detail = "User not found"
