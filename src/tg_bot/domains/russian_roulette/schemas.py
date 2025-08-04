from pydantic import BaseModel


class BadPhraseMessage(BaseModel):
    phrase: str
