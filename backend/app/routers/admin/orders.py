"""
Admin Orders router — 訂單管理 API
GET  /admin/orders
GET  /admin/orders/:id
PUT  /admin/orders/:id/status
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.admin_dependencies import require_admin_permission
from app.models.order import Order, OrderItem, OrderStatusLog
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.order import OrderStatusUpdate
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin/orders", tags=["管理後台 - 訂單"])

VALID_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["processing", "cancelled"],
    "processing": ["shipped", "cancelled"],
    "shipped": ["delivered"],
    "delivered": ["return_requested"],
    "return_requested": ["returned", "delivered"],
    "returned": [],
    "cancelled": [],
}


@router.get("", response_model=SuccessResponse)
async def list_orders(
    status_filter: Optional[str] = Query(default=None, alias="status"),
    payment_status: Optional[str] = None,
    q: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    _=Depends(require_admin_permission("orders.read")),
    db: AsyncSession = Depends(get_db),
):
    """列出所有訂單"""
    query = (
        select(Order)
        .options(selectinload(Order.user))
        .order_by(Order.created_at.desc())
    )

    if status_filter:
        query = query.where(Order.status == status_filter)
    if payment_status:
        query = query.where(Order.payment_status == payment_status)
    if q:
        search_term = f"%{q}%"
        query = query.where(Order.order_number.ilike(search_term))

    items, meta = await paginate(db, query, page, per_page)

    data = [
        {
            "id": o.id,
            "order_number": o.order_number,
            "user_email": o.user.email if o.user else None,
            "user_name": o.user.name if o.user else None,
            "status": o.status,
            "subtotal": float(o.subtotal),
            "discount": float(o.discount),
            "shipping_fee": float(o.shipping_fee),
            "total": float(o.total),
            "payment_method": o.payment_method,
            "payment_status": o.payment_status,
            "tracking_number": o.tracking_number,
            "created_at": o.created_at.isoformat(),
        }
        for o in items
    ]

    return SuccessResponse(data=data, meta=meta)


@router.get("/{order_id}", response_model=SuccessResponse)
async def get_order(
    order_id: int,
    _=Depends(require_admin_permission("orders.read")),
    db: AsyncSession = Depends(get_db),
):
    """取得訂單詳情"""
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.user),
            selectinload(Order.items),
            selectinload(Order.status_logs),
        )
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="訂單不存在")

    return SuccessResponse(data={
        "id": order.id,
        "order_number": order.order_number,
        "user": {
            "id": order.user.id,
            "email": order.user.email,
            "name": order.user.name,
        } if order.user else None,
        "status": order.status,
        "subtotal": float(order.subtotal),
        "discount": float(order.discount),
        "shipping_fee": float(order.shipping_fee),
        "total": float(order.total),
        "points_used": order.points_used,
        "credits_used": float(order.credits_used),
        "coupon_code": order.coupon_code,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "shipping_address": order.shipping_address,
        "tracking_number": order.tracking_number,
        "note": order.note,
        "items": [
            {
                "id": oi.id,
                "product_id": oi.product_id,
                "product_name": oi.product_name,
                "product_image": oi.product_image,
                "product_sku": oi.product_sku,
                "unit_price": float(oi.unit_price),
                "quantity": oi.quantity,
                "total_price": float(oi.total_price),
            }
            for oi in order.items
        ],
        "status_logs": [
            {
                "from_status": log.from_status,
                "to_status": log.to_status,
                "note": log.note,
                "created_at": log.created_at.isoformat(),
            }
            for log in order.status_logs
        ],
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
    })


@router.put("/{order_id}/status", response_model=SuccessResponse)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    _=Depends(require_admin_permission("orders.write")),
    db: AsyncSession = Depends(get_db),
):
    """更新訂單狀態"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="訂單不存在")

    allowed = VALID_TRANSITIONS.get(order.status, [])
    if data.status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"無法從 {order.status} 變更為 {data.status}",
        )

    old_status = order.status
    order.status = data.status

    if data.tracking_number:
        order.tracking_number = data.tracking_number

    db.add(OrderStatusLog(
        order_id=order.id,
        from_status=old_status,
        to_status=data.status,
        note=data.note or f"狀態變更: {old_status} → {data.status}",
    ))

    return SuccessResponse(data={"message": f"訂單狀態已更新為 {data.status}"})
