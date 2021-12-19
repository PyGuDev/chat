import uuid

import settings

from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from core.auth.utils import verify_password, create_token, ALGORITHM
from user import models
from user.schemas import Token, TokenData, SavedToken


def save_token(db: Session, item: SavedToken) -> SavedToken:
    token = models.Token(**item.dict())
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def get_user(db: Session, username: str):
    return db.query(models.User).filter(getattr(models.User, settings.USER_USERNAME_FIELD) == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def authenticate(db: Session, username: str, password: str) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, refresh_token = create_token(
        data={"sub": getattr(user, settings.USER_USERNAME_FIELD)}, expires_delta=access_token_expires
    )
    token = SavedToken(
        uid=uuid.uuid4().__str__(),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_date=datetime.now() + access_token_expires,
        token_type='Bearer')
    token = save_token(db, token)
    resp_token = Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type
    )
    return resp_token


def get_current_user(db: Session, token: str):
    token = token.strip('Bearer').strip(' ')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
