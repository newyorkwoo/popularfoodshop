"""
Admin Users router — 會員管理 API
GET  /admin/users
GET  /admin/users/:id
PUT  /admin/users/:id
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_permission
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.user import UserAdminUpdate
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin/users", tags=["管理後台 - 會員"])


@router.get("", response_model=SuccessResponse)
async def list_users(
    q: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    _=Depends(require_permission("users.read")),
    db: AsyncSession = Depends(get_db),
):
    """列出所有會員"""
    query = select(User).order_by(User.created_at.desc())

    if q:
        search_term = f"%{q}%"
        query = query.where(
            or_(User.email.ilike(search_term), User.name.ilike(search_term), User.phone.ilike(search_term))
        )
    if role:
        query = query.where(User.role == role)
    if is_active is not None:
        query = query.where(User.is_active == is_active)

    items, meta = await paginate(db, query, page, per_page)

    data = [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "phone": u.phone,
            "role": u.role,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "points": u.points,
            "credits": float(u.credits),
            "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
            "created_at": u.created_at.isoformat(),
        }
        for u in items
    ]

    return SuccessResponse(data=data, meta=meta)


@router.get("/{user_id}", response_model=SuccessResponse)
async def get_user(
    user_id: int,
    _=Depends(require_permission("users.read")),
    db: AsyncSession = Depends(get_db),
):
    """取得會員詳情"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="會員不存在")

    return SuccessResponse(data={
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "phone": user.phone,
        "avatar": user.avatar,
        "gender": user.gender,
        "birthday": user.birthday.isoformat() if user.birthday else None,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "points": user.points,
        "credits": float(user.credits),
        "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    })


@router.put("/{user_id}", response_model=SuccessResponse)
async def update_user(
    user_id: int,
    data: UserAdminUpdate,
    _=Depends(require_permission("users.write")),
    db: AsyncSession = Depends(get_db),
):
    """管理員更新會員資料"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="會員不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    return SuccessResponse(data={"id": user.id}, message="會員資料已更新")
