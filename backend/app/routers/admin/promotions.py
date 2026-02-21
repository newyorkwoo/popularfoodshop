"""
Admin Promotions router — 促銷/優惠券管理 API
GET    /admin/promotions/coupons
POST   /admin/promotions/coupons
GET    /admin/promotions/coupons/:id
PUT    /admin/promotions/coupons/:id
DELETE /admin/promotions/coupons/:id
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_permission
from app.models.coupon import Coupon
from app.schemas.common import SuccessResponse
from app.schemas.order import CouponCreate, CouponUpdate
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin/promotions", tags=["管理後台 - 促銷"])


@router.get("/coupons", response_model=SuccessResponse)
async def list_coupons(
    is_active: Optional[bool] = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    _=Depends(require_permission("promotions.read")),
    db: AsyncSession = Depends(get_db),
):
    """列出所有優惠券"""
    query = select(Coupon).order_by(Coupon.created_at.desc())
    if is_active is not None:
        query = query.where(Coupon.is_active == is_active)

    items, meta = await paginate(db, query, page, per_page)

    data = [
        {
            "id": c.id,
            "code": c.code,
            "description": c.description,
            "discount_type": c.discount_type,
            "discount_value": float(c.discount_value),
            "min_order_amount": float(c.min_order_amount) if c.min_order_amount else None,
            "max_discount_amount": float(c.max_discount_amount) if c.max_discount_amount else None,
            "usage_limit": c.usage_limit,
            "used_count": c.used_count,
            "is_active": c.is_active,
            "starts_at": c.starts_at.isoformat() if c.starts_at else None,
            "expires_at": c.expires_at.isoformat() if c.expires_at else None,
            "created_at": c.created_at.isoformat(),
        }
        for c in items
    ]

    return SuccessResponse(data=data, meta=meta)


@router.post("/coupons", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    data: CouponCreate,
    _=Depends(require_permission("promotions.write")),
    db: AsyncSession = Depends(get_db),
):
    """新增優惠券"""
    # Check code uniqueness
    existing = await db.execute(
        select(Coupon).where(Coupon.code == data.code.upper())
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="優惠券代碼已存在")

    coupon = Coupon(
        code=data.code.upper(),
        description=data.description,
        discount_type=data.discount_type,
        discount_value=data.discount_value,
        min_order_amount=data.min_order_amount,
        max_discount_amount=data.max_discount_amount,
        usage_limit=data.usage_limit,
        applicable_products=data.applicable_products,
        is_active=data.is_active if data.is_active is not None else True,
        starts_at=data.starts_at,
        expires_at=data.expires_at,
    )
    db.add(coupon)
    await db.flush()

    return SuccessResponse(data={"id": coupon.id, "code": coupon.code}, message="優惠券已建立")


@router.get("/coupons/{coupon_id}", response_model=SuccessResponse)
async def get_coupon(
    coupon_id: int,
    _=Depends(require_permission("promotions.read")),
    db: AsyncSession = Depends(get_db),
):
    """取得優惠券詳情"""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="優惠券不存在")

    return SuccessResponse(data={
        "id": coupon.id,
        "code": coupon.code,
        "description": coupon.description,
        "discount_type": coupon.discount_type,
        "discount_value": float(coupon.discount_value),
        "min_order_amount": float(coupon.min_order_amount) if coupon.min_order_amount else None,
        "max_discount_amount": float(coupon.max_discount_amount) if coupon.max_discount_amount else None,
        "usage_limit": coupon.usage_limit,
        "used_count": coupon.used_count,
        "applicable_products": coupon.applicable_products,
        "is_active": coupon.is_active,
        "starts_at": coupon.starts_at.isoformat() if coupon.starts_at else None,
        "expires_at": coupon.expires_at.isoformat() if coupon.expires_at else None,
        "created_at": coupon.created_at.isoformat(),
    })


@router.put("/coupons/{coupon_id}", response_model=SuccessResponse)
async def update_coupon(
    coupon_id: int,
    data: CouponUpdate,
    _=Depends(require_permission("promotions.write")),
    db: AsyncSession = Depends(get_db),
):
    """更新優惠券"""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="優惠券不存在")

    update_data = data.model_dump(exclude_unset=True)
    if "code" in update_data:
        update_data["code"] = update_data["code"].upper()
    for field, value in update_data.items():
        setattr(coupon, field, value)

    return SuccessResponse(data={"id": coupon.id}, message="優惠券已更新")


@router.delete("/coupons/{coupon_id}", response_model=SuccessResponse)
async def delete_coupon(
    coupon_id: int,
    _=Depends(require_permission("promotions.delete")),
    db: AsyncSession = Depends(get_db),
):
    """停用優惠券"""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="優惠券不存在")

    coupon.is_active = False
    return SuccessResponse(data={"message": "優惠券已停用"})
