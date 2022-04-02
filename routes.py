from fastapi.routing import APIRouter

from chat import chat
from user import user
from websocket.controllers import router as ws_router

routes = APIRouter()

routes.include_router(chat.router, prefix='/chat')
routes.include_router(user.router, prefix='/user')
routes.include_router(ws_router, prefix='/ws')
