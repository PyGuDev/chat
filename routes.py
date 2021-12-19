from fastapi.routing import APIRouter

from chat import chat
from user import user

routes = APIRouter()

routes.include_router(chat.router, prefix='/chat')
routes.include_router(user.router, prefix='/user')
