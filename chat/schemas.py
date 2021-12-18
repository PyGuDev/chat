from datetime import datetime

from pydantic import BaseModel
from pydantic.types import UUID4
from typing import Optional


class User(BaseModel):
    uid: UUID4
    name: str
    phone: str

    class Config:
        orm_mode = True


class BaseDialog(BaseModel):
    uid: UUID4
    name: str

    class Config:
        orm_mode = True


class ResponseDialog(BaseDialog):
    pass


class Message(BaseModel):
    dialog_uid: UUID4
    text: str
    created_at: Optional[datetime]
    readed: Optional[bool]
    sended: Optional[bool]
    author_uid: UUID4

    class Config:
        orm_mode = True