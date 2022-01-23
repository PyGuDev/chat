import uuid
from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette import status

from chat.schemas import ResponseDialog, ResponseMessagesSchema, UserOrDialogSchema, ResponseDialogId, \
    CreateMessageSchema, Message
from core.utils import get_db, get_user_from_request
from chat import crud
from user import crud as crud_user

router = APIRouter()


@router.get('/dialog', response_model=List[ResponseDialog])
def get_dialogs(db: Session = Depends(get_db), user=Depends(get_user_from_request)):
    """
    Возвращаем список диалогов
    """
    dialogs = crud.get_dialogs(db, user.uid)
    for dialog in dialogs:
        for dialog_user in dialog.users:
            if dialog_user.user_id != user.uid:
                dialog.name = dialog_user.user.name
    return dialogs


@router.post('/dialog', response_model=ResponseDialogId)
def create_dialog(item: UserOrDialogSchema, db: Session = Depends(get_db), user=Depends(get_user_from_request)):
    """
    Создание диалога
    На вход принимает:
     phone - номер телефона собеседника или
     dialog_id - индефикатор диалога
    """
    if item.phone is not None and item.dialog_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': 'invalid params. Send phone or dialog_id'}
        )
    else:
        if item.phone:
            companion = crud_user.get_user_by_phone(db, item.phone)
            if companion is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'message': 'user with is phone not found'}
                )
            dialog = crud.create_dialog(db, None)
            crud.create_user_dialog(db, user.uid, dialog.uid)
            crud.create_user_dialog(db, companion.uid, dialog.uid)
            return ResponseDialogId(dialog_id=dialog.uid).dict()
        else:
            crud.create_user_dialog(user.uid, item.dialog_id)
            return ResponseDialogId(dialog_id=item.dialog_id).dict()


@router.get('/dialog/{dialog_id}/message', response_model=List[ResponseMessagesSchema])
def get_messages(dialog_id: str, db: Session = Depends(get_db), user=Depends(get_user_from_request)):
    """
    Возвращаем список диалогов
    """
    messages = crud.get_messages(db, dialog_id, user.uid)
    return messages


@router.post('/dialog/{dialog_id}/message', response_model=ResponseMessagesSchema)
def create_message(
        dialog_id: str, message: CreateMessageSchema,
        db: Session = Depends(get_db), user=Depends(get_user_from_request)):
    message_data = Message(
        uid=uuid.uuid4().__str__(),
        text=message.text,
        created_at=datetime.now(),
        readed=False,
        author_id=user.uid,
        dialog_id=dialog_id
    )

    message = crud.create_message(db, message_data)
    return message
