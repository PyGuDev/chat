from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from starlette.websockets import WebSocket

from core.db import SessionLocal
from routes import routes
from user.authenticate import get_user_by_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Union[Request, WebSocket], call_next):
    response = Response("Internal server error", status_code=500)

    try:
        request.state.db = SessionLocal()
        if 'authorization' in list(request.headers.keys()):
            token = request.headers.get('Authorization')
            if token:
                user = get_user_by_token(request.state.db, token)
                request.state.user = user
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN
                )
        response = await call_next(request)
    except HTTPException as http_exc:
        response = Response(http_exc.detail, status_code=http_exc.status_code)

    finally:
        request.state.db.close()

    return response


app.include_router(routes, prefix='/api/v1')
