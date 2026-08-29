from fastapi import Depends, HTTPException, Request, status

from agriflow.security import SESSION_COOKIE_NAME, read_session_token


def get_env(request: Request):
    return request.scope["env"]


def get_current_user(request: Request) -> dict:
    env = get_env(request)
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")

    session = read_session_token(env.SESSION_SECRET, token)
    if session is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session expired or invalid")

    return session


def require_master(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "master":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Master access required")
    return user
