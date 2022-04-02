import asyncio
from typing import Optional

from fastapi import APIRouter, Depends
from starlette.concurrency import run_until_first_complete
from starlette.websockets import WebSocket, WebSocketDisconnect

from user.models import User
from websocket.manager import ChannelManager
from websocket.utilities import get_user_by_token

router = APIRouter()
manager = ChannelManager()


@router.websocket("/connect/{dialog_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        dialog_id: str,
        user: Optional[User] = Depends(get_user_by_token),
):
    if user:
        try:
            await websocket.accept()
            await run_until_first_complete(
                (ws_receiver, {"channel_name": dialog_id, "websocket": websocket}),
                (ws_sender, {"channel_name": dialog_id, "websocket": websocket})
            )

        except WebSocketDisconnect:
            await websocket.close()
    else:
        await websocket.send_text("Disconnect")
        await websocket.close()


async def ws_receiver(channel_name, websocket):
    while True:
        text_msg = await websocket.receive_text()
        if text_msg:
            await manager.send(channel_name, text_msg)


async def ws_sender(channel_name, websocket):
    channel = await manager.subscribe_channel(channel_name)
    while True:
        message = await channel.get_message()
        if message and message.get('data') != 1:
            text_message = message.get('data').decode('utf-8')
            await websocket.send_text(text_message)
        await asyncio.sleep(0.01)
