from pydantic import BaseModel


class CarInput(BaseModel):
    make: str
    model: str
    uid: str


class CarDetailsInput(BaseModel):
    make: str = None
    model: str = None
