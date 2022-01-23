from sqlalchemy.orm import Session

from user.schemas import CreateUser
from user.models import User


def create_user(db: Session, item: CreateUser) -> User:
    user = User(**item.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_phone(db: Session, phone: str) -> User:
    user = db.query(User).filter(User.phone == phone).first()
    return user
