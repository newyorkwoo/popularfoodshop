"""
Admin Security utilities — Separate JWT tokens for admin panel
Uses different secret key and shorter expiry for enhanced security
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


def create_admin_access_token(
    user_id: int,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create an admin JWT access token (separate secret, shorter expiry)"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "admin_access",
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(payload, settings.ADMIN_JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_admin_refresh_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create an admin JWT refresh token"""
    if expires_delta is None:
        expires_delta = timedelta(days=settings.ADMIN_REFRESH_TOKEN_EXPIRE_DAYS)

    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    payload = {
        "sub": str(user_id),
        "type": "admin_refresh",
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(payload, settings.ADMIN_JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_admin_token(token: str) -> Optional[dict]:
    """Decode and validate an admin JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.ADMIN_JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None
