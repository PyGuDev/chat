import uuid
from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

import settings
from core.auth.utils import verify_password, create_token, ALGORITHM, reverse_token
from user import models
from user.schemas import Token, TokenData, SavedToken, UpdateToken


def save_token(db: Session, item: SavedToken):
    token = models.Token(**item.dict())
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def update_token(db: Session, item: UpdateToken, id: str):
    db.query(models.Token).filter(models.Token.uid == id). \
        update(item.dict())
    db.commit()


def get_user(db: Session, user_id: Optional[str] = None, username: Optional[str] = None):
    if user_id:
        return db.query(models.User).filter(getattr(models.User, settings.USER_ID_FIELD) == user_id).first()
    if username:
        return db.query(models.User).filter(getattr(models.User, settings.USER_USERNAME_FIELD) == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_token_for_user(db: Session, user_id: str):
    return db.query(models.Token).filter(models.Token.user_id == user_id).first()


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
        data={"sub": getattr(user, settings.USER_ID_FIELD)}, expires_delta=access_token_expires
    )

    token_from_model = get_token_for_user(db, user.uid)

    expires_date = datetime.now() + access_token_expires
    print(f"token - {token_from_model}")
    if token_from_model:

        token = UpdateToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_date=expires_date,
            token_type='Bearer'
        )
        update_token(db, token, token_from_model.uid)
    else:
        token = SavedToken(
            uid=uuid.uuid4().__str__(),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_date=expires_date,
            user_id=user.uid,
            token_type='Bearer')
        save_token(db, token)

    resp_token = Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
        expires_date=expires_date
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
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


def refresh(db: Session, refresh_token: str):
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = TokenData(user_id=user_id)
    user = get_user(db, user_id=token_data.user_id)
    if user:
        token = get_token_for_user(db, user.uid)
        if token.refresh_token == refresh_token:
            access_token = reverse_token(payload, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
            update_token_data = UpdateToken(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer",
                expires_date=datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            update_token(db, update_token_data, token.uid)
            return update_token_data
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return None
