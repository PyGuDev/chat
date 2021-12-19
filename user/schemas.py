from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True


class SavedToken(Token):
    uid: str
    expires_date: datetime


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    name: str
    phone: str

    class Config:
        orm_mode = True


class SingUp(User):
    password: str


class SignIn(BaseModel):
    phone: str
    password: str


class CreateUser(User):
    uid: str
    hashed_password: str
    is_active: bool = True


class ResponseUser(User):
    uid: UUID
