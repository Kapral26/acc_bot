from fastapi import HTTPException
from starlette import status


class PhraseAlreadyExist(HTTPException):
    def __init__(self, detail: str = "Фраза уже существует, а вот ты не уверен."):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)

