from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from user.authenticate import get_current_user
from core.db import SessionLocal
from routes import routes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)

    try:
        request.state.db = SessionLocal()
        
        if 'authorization' in list(request.headers.keys()):
            token = request.headers.get('Authorization')
            if token:
                user = get_current_user(request.state.db, token)
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
