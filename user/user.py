import uuid

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from user.schemas import SingUp, SignIn, CreateUser, ResponseUser
from core.auth.utils import get_password_hash
from user.authenticate import authenticate, Token
from core.utils import get_db
from user import crud

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
    user = crud.create_user(db, user)
    return user


@router.post('/signin', response_model=Token)
def login_user(item: SignIn, db: Session = Depends(get_db)):
    token = authenticate(db, item.phone, item.password)
    return token
