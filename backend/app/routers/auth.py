"""
Auth router — 認證相關 API
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
POST /auth/forgot-password
POST /auth/reset-password
GET  /auth/me
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.points import PointsTransaction
from app.schemas.user import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.common import SuccessResponse
from app.utils.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    verify_password_reset_token,
)

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["認證"])


@router.post("/register", response_model=SuccessResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """註冊新帳號"""
    # Check existing email
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="此 Email 已被註冊",
        )

    # Create user
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        role="customer",
        is_active=True,
        points=settings.REGISTER_BONUS_POINTS,
    )
    db.add(user)
    await db.flush()

    # Record registration bonus points
    if settings.REGISTER_BONUS_POINTS > 0:
        points_tx = PointsTransaction(
            user_id=user.id,
            type="earn",
            amount=settings.REGISTER_BONUS_POINTS,
            balance_after=settings.REGISTER_BONUS_POINTS,
            reference_type="register",
            description="註冊獎勵",
        )
        db.add(points_tx)

    # Generate tokens
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        message="註冊成功",
    )


@router.post("/login", response_model=SuccessResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """登入"""
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

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        message="登入成功",
    )


@router.post("/refresh", response_model=SuccessResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """刷新 Token"""
    payload = decode_token(data.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的 Refresh Token",
        )

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者不存在或已停用",
        )

    access_token = create_access_token(user.id, user.role)
    new_refresh_token = create_refresh_token(user.id)

    return SuccessResponse(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).model_dump(),
        message="Token 刷新成功",
    )


@router.post("/logout", response_model=SuccessResponse)
async def logout(current_user=Depends(get_current_user)):
    """登出（前端清除 Token、後端可加入黑名單）"""
    # TODO: Add token to Redis blacklist for true invalidation
    return SuccessResponse(message="登出成功")


@router.post("/forgot-password", response_model=SuccessResponse)
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """忘記密碼 — 寄送重設密碼信"""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    if user:
        token = create_password_reset_token(user.email)
        # TODO: Send password reset email via Celery task
        # send_password_reset_email.delay(user.email, token)

    return SuccessResponse(message="如果此 Email 已註冊，將會收到重設密碼信")


@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """重設密碼"""
    email = verify_password_reset_token(data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無效或已過期的重設連結",
        )

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="使用者不存在",
        )

    user.password_hash = hash_password(data.password)

    return SuccessResponse(message="密碼重設成功，請重新登入")


@router.get("/me", response_model=SuccessResponse)
async def get_me(current_user=Depends(get_current_user)):
    """取得當前使用者資訊"""
    return SuccessResponse(
        data=UserResponse.model_validate(current_user).model_dump(),
    )
