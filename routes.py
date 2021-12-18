from fastapi.routing import APIRouter

from chat import chat


routes = APIRouter()

routes.include_router(chat.router, prefix='/chat')
