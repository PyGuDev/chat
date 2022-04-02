from typing import Optional

from fastapi import Query
from starlette import status
from starlette.websockets import WebSocket

from core.db import SessionLocal
from user.authenticate import authenticate_by_token_for_ws


async def get_user_by_token(
        websocket: WebSocket,
        token: Optional[str] = Query(None),
):
    """Получить пользователя по токену"""
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
    else:
        db = SessionLocal()
        user = authenticate_by_token_for_ws(db, token)
        return user
