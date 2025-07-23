
from pydantic import BaseModel


class AnalyticsSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class AnalyticsSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True