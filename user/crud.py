from sqlalchemy.orm import Session

from user.schemas import CreateUser
from user.models import User


def create_user(db: Session, item: CreateUser):
    user = User(**item.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user