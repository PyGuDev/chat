from datetime import timedelta, datetime
from typing import Optional, Tuple

from jose import jwt
from passlib.context import CryptContext

import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> Tuple[str, str]:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    to_encode.update({"token": access_token})
    to_encode.pop("exp")
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return access_token, refresh_token


def reverse_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.pop("token")
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return access_token
