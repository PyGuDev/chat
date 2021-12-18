from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from chat.schemas import ResponseDialog
from core.utils import get_db
from chat import crud

router = APIRouter()


@router.get('', response_model=List[ResponseDialog])
def get_dialogs(db: Session = Depends(get_db)):
    """
    Возвращаем список диалогов
    """
    dialogs = crud.get_dialogs(db)
    return dialogs

