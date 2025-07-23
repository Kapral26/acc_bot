from pydantic import BaseModel


class BadPhraseSchema(BaseModel):
    id: int
    phrase: str

    class Config:
        from_attributes = True

class BadPhraseCRUD(BaseModel):
    phrase: str

    class Config:
        from_attributes = True