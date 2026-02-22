"""
Admin Auth router — 管理後台獨立認證 API
POST /admin/auth/login          — 管理員登入（僅限 admin 角色）
POST /admin/auth/refresh        — 刷新管理員 Token
POST /admin/auth/logout         — 管理員登出
GET  /admin/auth/me             — 取得管理員資訊
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin_dependencies import check_admin_ip, get_current_admin_user
from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.user import LoginRequest, TokenResponse
from app.utils.admin_security import (
    create_admin_access_token,
    create_admin_refresh_token,
    decode_admin_token,
)
from app.utils.security import verify_password

settings = get_settings()
router = APIRouter(prefix="/admin/auth", tags=["管理後台 - 認證"])

ADMIN_ROLES = ("super_admin", "admin", "editor")


@router.post("/login", response_model=SuccessResponse)
async def admin_login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """管理員登入（使用獨立 JWT secret，僅限管理員角色）"""
    # IP whitelist check
    await check_admin_ip(request)

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email 或密碼錯誤",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="帳號已被停用",
        )

    # Only admin roles can login to admin panel
    if user.role not in ADMIN_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此帳號無管理員權限",
        )

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)

    # Generate admin-specific tokens (separate secret key)
    access_token = create_admin_access_token(user.id, user.role)
    refresh_token = create_admin_refresh_token(user.id)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        message="管理員登入成功",
    )


@router.post("/refresh", response_model=SuccessResponse)
async def admin_refresh_token(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """刷新管理員 Token"""
    await check_admin_ip(request)

    # Get refresh token from request body
    body = await request.json()
    token = body.get("refresh_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少 refresh_token",
        )

    payload = decode_admin_token(token)

    if not payload or payload.get("type") != "admin_refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的管理員 Refresh Token",
        )

    user_id = int(payload.get("sub"))
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者不存在或已停用",
        )

    if user.role not in ADMIN_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此帳號無管理員權限",
        )

    access_token = create_admin_access_token(user.id, user.role)
    new_refresh_token = create_admin_refresh_token(user.id)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        message="Token 刷新成功",
    )


@router.post("/logout", response_model=SuccessResponse)
async def admin_logout(current_admin=Depends(get_current_admin_user)):
    """管理員登出"""
    # TODO: Add admin token to Redis blacklist
    return SuccessResponse(message="管理員登出成功")


@router.get("/me", response_model=SuccessResponse)
async def admin_me(current_admin=Depends(get_current_admin_user)):
    """取得當前管理員資訊"""
    return SuccessResponse(
        data={
            "id": current_admin.id,
            "email": current_admin.email,
            "first_name": current_admin.first_name,
            "last_name": current_admin.last_name,
            "role": current_admin.role,
            "phone": current_admin.phone or "",
            "is_active": current_admin.is_active,
        }
    )
