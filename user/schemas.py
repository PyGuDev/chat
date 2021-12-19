from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_date: datetime

    class Config:
        orm_mode = True


class SavedToken(Token):
    uid: str
    expires_date: datetime
    user_id: str


class UpdateToken(Token):
    expires_date: datetime


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


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
