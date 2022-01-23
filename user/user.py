import uuid

import sqlalchemy
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette import status

from core.auth.utils import get_password_hash
from core.utils import get_db
from user import crud
from user.authenticate import authenticate, Token, refresh
from user.schemas import SingUp, SignIn, CreateUser, ResponseUser, RefreshToken

router = APIRouter()


@router.post('/signup', response_model=ResponseUser)
def register_user(item: SingUp, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(item.password)

    user = CreateUser(
        uid=uuid.uuid4().__str__(),
        name=item.name,
        phone=item.phone,
        hashed_password=hashed_password
    )
    try:
        user = crud.create_user(db, user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post('/signin', response_model=Token)
def login_user(item: SignIn, db: Session = Depends(get_db)):
    token = authenticate(db, item.phone, item.password)
    return token


@router.post('/refresh')
def refresh_token(item: RefreshToken, db: Session = Depends(get_db)):
    token = refresh(db, item.refresh_token)
    return token
