"""
Admin Dependencies — Separate authentication for admin panel
Uses independent JWT secret and IP whitelist enforcement
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db

settings = get_settings()
admin_security_scheme = HTTPBearer(auto_error=False)

ADMIN_ROLES = ("super_admin", "admin", "editor")

ROLE_PERMISSIONS = {
    "super_admin": ["*"],
    "admin": [
        "products.read", "products.write", "products.delete",
        "orders.read", "orders.write",
        "users.read", "users.write",
        "content.read", "content.write", "content.delete",
        "promotions.read", "promotions.write", "promotions.delete",
        "reports.read",
        "settings.read", "settings.write", "settings.delete",
    ],
    "editor": [
        "products.read", "products.write",
        "content.read", "content.write",
        "orders.read",
    ],
    "viewer": [
        "products.read",
        "orders.read",
        "users.read",
        "reports.read",
    ],
}


def _get_client_ip(request: Request) -> str:
    """Extract client IP, respecting X-Forwarded-For behind proxy"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def check_admin_ip(request: Request):
    """Enforce IP whitelist for admin panel access"""
    if not settings.ADMIN_ALLOWED_IPS:
        return  # Empty = no restriction (development mode)

    client_ip = _get_client_ip(request)
    if client_ip not in settings.ADMIN_ALLOWED_IPS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此 IP 不允許存取管理後台",
        )


async def get_current_admin_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(admin_security_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate admin user using ADMIN-specific JWT token.
    - Uses separate ADMIN_JWT_SECRET_KEY
    - Validates token type is 'admin_access'
    - Checks admin role
    - Enforces IP whitelist
    """
    # IP whitelist check
    await check_admin_ip(request)

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
            settings.ADMIN_JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id_str = payload.get("sub")
        user_id = int(user_id_str) if user_id_str else None
        token_type: str = payload.get("type", "")
        role: str = payload.get("role", "")

        # Must be an admin-specific token
        if user_id is None or token_type != "admin_access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無效的管理員 Token",
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
            detail="無效的管理員 Token",
        )

    # Fetch user from DB
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

    if user.role not in ADMIN_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="權限不足，需要管理員權限",
        )

    return user


def require_admin_permission(permission: str):
    """Admin permission check dependency factory"""

    async def check_permission(
        current_user=Depends(get_current_admin_user),
    ):
        role_perms = ROLE_PERMISSIONS.get(current_user.role, [])

        if "*" not in role_perms and permission not in role_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"權限不足，需要 {permission} 權限",
            )
        return current_user

    return check_permission
