import uuid
from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette import status

from chat.helpers import is_valid_user
from chat.schemas import ResponseDialog, ResponseMessagesSchema, UserOrDialogSchema, ResponseDialogId, \
    CreateMessageSchema, Message
from core.utils import get_db, get_user_from_request
from chat import crud
from user import crud as crud_user
from websocket.manager import ChannelManager

router = APIRouter()
channel_manager = ChannelManager()


@router.get('/dialog', response_model=List[ResponseDialog])
def get_dialogs(db: Session = Depends(get_db), user=Depends(get_user_from_request)):
    """
    Возвращаем список диалогов
    """
    is_valid_user(user)

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
    is_valid_user(user)

    if item.phone is not None and item.dialog_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': 'invalid params. Send phone or dialog_id'}
        )
    else:
        if item.phone:
            if item.phone == user.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={'message': 'user with is phone not found'}
                )
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
            crud.create_user_dialog(db, user.uid, item.dialog_id)
            return ResponseDialogId(dialog_id=item.dialog_id).dict()


@router.get('/dialog/{dialog_id}/message', response_model=List[ResponseMessagesSchema])
def get_messages(dialog_id: str, db: Session = Depends(get_db), user=Depends(get_user_from_request)):
    """
    Возвращаем список диалогов
    """
    is_valid_user(user)

    messages = crud.get_messages(db, dialog_id, user.uid)
    new_data = list()
    for msg in messages:
        copy_msg = msg.__dict__
        copy_msg['me'] = False if msg.author_id == user.uid else True
        new_data.append(copy_msg)
    return new_data


@router.post('/dialog/{dialog_id}/message', response_model=ResponseMessagesSchema)
async def create_message(
        dialog_id: str, message: CreateMessageSchema,
        db: Session = Depends(get_db), user=Depends(get_user_from_request)):

    is_valid_user(user)

    message_data = Message(
        uid=uuid.uuid4().__str__(),
        text=message.text,
        created_at=datetime.now(),
        readed=False,
        author_id=user.uid,
        dialog_id=dialog_id
    )

    message = crud.create_message(db, message_data)
    msg_dict = message.__dict__
    response = ResponseMessagesSchema(**msg_dict)
    try:
        await channel_manager.send(dialog_id, response.json())
    except Exception as exc:
        print(f"send_message error: {exc}")
    return response

