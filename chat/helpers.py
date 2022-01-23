from fastapi import HTTPException
from starlette import status


def is_valid_user(user: any):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
