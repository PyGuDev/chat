from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class BaseDialog(BaseModel):
    uid: UUID
    name: str

    class Config:
        orm_mode = True


class ResponseDialog(BaseDialog):
    pass


class Message(BaseModel):
    dialog_uid: UUID
    text: str
    created_at: Optional[datetime]
    readed: Optional[bool]
    sended: Optional[bool]
    author_uid: UUID

    class Config:
        orm_mode = True