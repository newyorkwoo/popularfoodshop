"""
Admin Settings router — 系統設定 API
GET /admin/settings
PUT /admin/settings
GET /admin/settings/shipping-methods
CRUD /admin/settings/shipping-methods
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_permission
from app.models.shipping import ShippingMethod
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/admin/settings", tags=["管理後台 - 設定"])


class ShippingMethodCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    fee: float
    free_threshold: Optional[float] = None
    estimated_days: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class ShippingMethodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fee: Optional[float] = None
    free_threshold: Optional[float] = None
    estimated_days: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


@router.get("/shipping-methods", response_model=SuccessResponse)
async def list_shipping_methods(
    _=Depends(require_permission("settings.read")),
    db: AsyncSession = Depends(get_db),
):
    """列出運送方式"""
    result = await db.execute(
        select(ShippingMethod).order_by(ShippingMethod.sort_order.asc())
    )
    methods = result.scalars().all()

    data = [
        {
            "id": m.id,
            "name": m.name,
            "code": m.code,
            "description": m.description,
            "fee": float(m.fee),
            "free_threshold": float(m.free_threshold) if m.free_threshold else None,
            "estimated_days": m.estimated_days,
            "is_active": m.is_active,
            "sort_order": m.sort_order,
        }
        for m in methods
    ]
    return SuccessResponse(data=data)


@router.post("/shipping-methods", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_shipping_method(
    data: ShippingMethodCreate,
    _=Depends(require_permission("settings.write")),
    db: AsyncSession = Depends(get_db),
):
    """新增運送方式"""
    existing = await db.execute(
        select(ShippingMethod).where(ShippingMethod.code == data.code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="運送代碼已存在")

    method = ShippingMethod(**data.model_dump())
    db.add(method)
    await db.flush()
    return SuccessResponse(data={"id": method.id}, message="運送方式已建立")


@router.put("/shipping-methods/{method_id}", response_model=SuccessResponse)
async def update_shipping_method(
    method_id: int,
    data: ShippingMethodUpdate,
    _=Depends(require_permission("settings.write")),
    db: AsyncSession = Depends(get_db),
):
    """更新運送方式"""
    result = await db.execute(
        select(ShippingMethod).where(ShippingMethod.id == method_id)
    )
    method = result.scalar_one_or_none()
    if not method:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="運送方式不存在")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(method, field, value)
    return SuccessResponse(data={"id": method.id}, message="運送方式已更新")


@router.delete("/shipping-methods/{method_id}", response_model=SuccessResponse)
async def delete_shipping_method(
    method_id: int,
    _=Depends(require_permission("settings.delete")),
    db: AsyncSession = Depends(get_db),
):
    """停用運送方式"""
    result = await db.execute(
        select(ShippingMethod).where(ShippingMethod.id == method_id)
    )
    method = result.scalar_one_or_none()
    if not method:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="運送方式不存在")

    method.is_active = False
    return SuccessResponse(data={"message": "運送方式已停用"})
