from sqlalchemy.orm import Session

from . import models, schemas


def get_dialogs(db: Session):
    return db.query(models.Dialog).all()
