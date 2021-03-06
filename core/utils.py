from starlette.requests import Request


def get_db(request: Request):
    return request.state.db


def get_user_from_request(request: Request):
    if hasattr(request.state, 'user'):
        return request.state.user
    else:
        return None
