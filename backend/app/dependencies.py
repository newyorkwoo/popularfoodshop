"""
Popular Food Shop — Shared Dependencies
JWT authentication, current user resolution, permissions
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db

settings = get_settings()
security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """取得當前已認證的使用者"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供認證憑證",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id_str = payload.get("sub")
        token_type: str = payload.get("type", "access")
        user_id = int(user_id_str) if user_id_str else None

        if user_id is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無效的認證 Token",
            )

        # Check expiry
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 已過期",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證 Token",
        )

    # Import here to avoid circular dependency
    from app.models.user import User

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者不存在",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="帳號已被停用",
        )

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """取得當前使用者（可選，未登入回傳 None）"""
    if credentials is None:
        return None

    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


async def get_current_admin(
    current_user=Depends(get_current_user),
):
    """取得當前管理員（需要 admin 或 super_admin 角色）"""
    if current_user.role not in ("admin", "super_admin", "editor"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="權限不足，需要管理員權限",
        )
    return current_user


def require_permission(permission: str):
    """權限檢查裝飾器工廠"""

    ROLE_PERMISSIONS = {
        "super_admin": ["*"],
        "admin": [
            "products:read", "products:write",
            "orders:read", "orders:write",
            "users:read", "users:write",
            "content:read", "content:write",
            "promotions:read", "promotions:write",
            "reports:read",
            "settings:read", "settings:write",
        ],
        "editor": [
            "products:read", "products:write",
            "content:read", "content:write",
            "orders:read",
        ],
        "viewer": [
            "products:read",
            "orders:read",
            "users:read",
            "reports:read",
        ],
    }

    async def check_permission(
        current_user=Depends(get_current_admin),
    ):
        role_perms = ROLE_PERMISSIONS.get(current_user.role, [])

        if "*" not in role_perms and permission not in role_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"權限不足，需要 {permission} 權限",
            )
        return current_user

    return check_permission
