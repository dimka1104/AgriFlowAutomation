from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from agriflow.db import (
    create_user,
    get_manageable_user,
    get_user_by_username,
    list_manageable_users,
    update_user_password,
    update_user_role,
)
from agriflow.deps import get_env, require_master
from agriflow.security import hash_password

router = APIRouter(prefix="/api/admin/users", tags=["admin-users"])

AssignableRole = Literal["user", "manager"]


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8)
    role: AssignableRole


class UpdateUserRequest(BaseModel):
    password: Optional[str] = Field(default=None, min_length=8)
    role: Optional[AssignableRole] = None


def _serialize(user) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at,
    }


@router.get("")
async def list_users(request: Request, master: dict = Depends(require_master)):
    users = await list_manageable_users(get_env(request))
    return [_serialize(u) for u in users]


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_user(
    payload: CreateUserRequest, request: Request, master: dict = Depends(require_master)
):
    env = get_env(request)
    if await get_user_by_username(env, payload.username) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already exists")

    user = await create_user(env, payload.username, hash_password(payload.password), payload.role)
    return _serialize(user)


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    payload: UpdateUserRequest,
    request: Request,
    master: dict = Depends(require_master),
):
    if payload.password is None and payload.role is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Provide a password and/or role to update")

    env = get_env(request)
    if await get_manageable_user(env, user_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if payload.password is not None:
        await update_user_password(env, user_id, hash_password(payload.password))
    if payload.role is not None:
        await update_user_role(env, user_id, payload.role)

    return _serialize(await get_manageable_user(env, user_id))
