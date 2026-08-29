from fastapi import APIRouter, Depends

from agriflow.deps import get_current_user, require_master

router = APIRouter(prefix="/api", tags=["main"])


@router.get("/dashboard")
async def dashboard(user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {user['username']}.", "role": user["role"]}


@router.get("/admin/ping")
async def admin_ping(user: dict = Depends(require_master)):
    return {"ok": True, "username": user["username"]}
