import uuid
from typing import Optional, List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models, schemas
from .schemas import Message


def get_dialogs(db: Session, user_id: str) -> List[models.Dialog]:
    return db.query(models.Dialog).join(models.UserDialog).filter(
        models.UserDialog.user_id == user_id).all()


def create_dialog(db: Session, name: Optional[str]):
    dialog = models.Dialog(uid=uuid.uuid4().__str__(), name=name)
    db.add(dialog)
    db.commit()
    db.refresh(dialog)
    return dialog


def create_user_dialog(db: Session, user_id: str, dialog_id: str):
    user_dialog = models.UserDialog(uid=uuid.uuid4().__str__(), user_id=user_id, dialog_id=dialog_id)
    db.add(user_dialog)
    db.commit()
    db.refresh(user_dialog)
    return user_dialog


def get_messages(db: Session, dialog_id: str, user_id: str) -> List[models.Message]:
    return db.query(models.Message).select_from(models.UserDialog).filter(
        models.Message.dialog_id == dialog_id,
        models.UserDialog.user_id == user_id
        ).order_by(desc(models.Message.created_at)).all()


def create_message(db: Session, data: Message) -> models.Message:
    message = models.Message(**data.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
