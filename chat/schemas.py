from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class BaseDialog(BaseModel):
    uid: str
    name: str

    class Config:
        orm_mode = True


class ResponseDialog(BaseDialog):
    pass


class ResponseDialogId(BaseModel):
    dialog_id: str


class CreateDialogSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CreateUserDialogSchema(BaseModel):
    user_id: str
    dialog_id: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    uid: str
    dialog_id: str
    text: str
    created_at: Optional[datetime]
    readed: Optional[bool]
    author_id: str

    class Config:
        orm_mode = True


class CreateMessageSchema(BaseModel):
    text: str

    class Config:
        orm_mode = True


class ResponseMessagesSchema(BaseModel):
    text: str
    created_at: Optional[datetime]
    readed: Optional[bool]
    author_id: str

    class Config:
        orm_mode = True


class UserOrDialogSchema(BaseModel):
    phone: Optional[str]
    dialog_id: Optional[str]
