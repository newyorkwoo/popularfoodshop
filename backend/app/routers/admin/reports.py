"""
Admin Reports router — 報表 API
GET /admin/reports/sales
GET /admin/reports/products
GET /admin/reports/users
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.admin_dependencies import require_admin_permission
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/admin/reports", tags=["管理後台 - 報表"])


@router.get("/sales", response_model=SuccessResponse)
async def sales_report(
    start_date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    group_by: str = Query(default="day", regex="^(day|week|month)$"),
    _=Depends(require_admin_permission("reports.read")),
    db: AsyncSession = Depends(get_db),
):
    """銷售報表"""
    if not start_date:
        start = datetime.utcnow() - timedelta(days=30)
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")

    if not end_date:
        end = datetime.utcnow()
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

    # Group function
    if group_by == "month":
        date_trunc = func.date_trunc("month", Order.created_at)
    elif group_by == "week":
        date_trunc = func.date_trunc("week", Order.created_at)
    else:
        date_trunc = func.date_trunc("day", Order.created_at)

    result = await db.execute(
        select(
            date_trunc.label("period"),
            func.count(Order.id).label("order_count"),
            func.coalesce(func.sum(Order.total), 0).label("revenue"),
            func.coalesce(func.sum(Order.discount), 0).label("total_discount"),
        )
        .where(
            Order.created_at >= start,
            Order.created_at < end,
            Order.payment_status == "paid",
        )
        .group_by(date_trunc)
        .order_by(date_trunc.asc())
    )
    rows = result.all()

    data = [
        {
            "period": r.period.isoformat() if r.period else None,
            "order_count": r.order_count,
            "revenue": float(r.revenue),
            "total_discount": float(r.total_discount),
        }
        for r in rows
    ]

    # Totals
    total_revenue = sum(d["revenue"] for d in data)
    total_orders = sum(d["order_count"] for d in data)

    return SuccessResponse(data={
        "summary": {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "avg_order_value": round(total_revenue / total_orders, 2) if total_orders else 0,
        },
        "chart_data": data,
    })


@router.get("/products", response_model=SuccessResponse)
async def products_report(
    limit: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="sold_count", regex="^(sold_count|revenue|view_count)$"),
    _=Depends(require_admin_permission("reports.read")),
    db: AsyncSession = Depends(get_db),
):
    """商品銷售報表"""
    if sort_by == "revenue":
        result = await db.execute(
            select(
                OrderItem.product_id,
                OrderItem.product_name,
                func.sum(OrderItem.quantity).label("total_sold"),
                func.sum(OrderItem.total_price).label("total_revenue"),
            )
            .group_by(OrderItem.product_id, OrderItem.product_name)
            .order_by(func.sum(OrderItem.total_price).desc())
            .limit(limit)
        )
        rows = result.all()
        data = [
            {
                "product_id": r.product_id,
                "product_name": r.product_name,
                "total_sold": r.total_sold,
                "total_revenue": float(r.total_revenue),
            }
            for r in rows
        ]
    else:
        sort_col = Product.sold_count if sort_by == "sold_count" else Product.view_count
        result = await db.execute(
            select(Product)
            .where(Product.is_active == True)
            .order_by(sort_col.desc())
            .limit(limit)
        )
        products = result.scalars().all()
        data = [
            {
                "product_id": p.id,
                "product_name": p.name,
                "sold_count": p.sold_count,
                "view_count": p.view_count,
                "stock": p.stock,
                "price": float(p.price),
            }
            for p in products
        ]

    return SuccessResponse(data=data)


@router.get("/users", response_model=SuccessResponse)
async def users_report(
    _=Depends(require_admin_permission("reports.read")),
    db: AsyncSession = Depends(get_db),
):
    """會員統計報表"""
    now = datetime.utcnow()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)
    last_90 = now - timedelta(days=90)

    total_result = await db.execute(select(func.count(User.id)))
    total = total_result.scalar() or 0

    active_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active = active_result.scalar() or 0

    new_7d = await db.execute(
        select(func.count(User.id)).where(User.created_at >= last_7)
    )
    new_30d = await db.execute(
        select(func.count(User.id)).where(User.created_at >= last_30)
    )

    active_buyers = await db.execute(
        select(func.count(func.distinct(Order.user_id))).where(Order.created_at >= last_90)
    )

    # Role breakdown
    role_result = await db.execute(
        select(User.role, func.count(User.id)).group_by(User.role)
    )
    role_breakdown = {r[0]: r[1] for r in role_result.all()}

    return SuccessResponse(data={
        "total_users": total,
        "active_users": active,
        "new_users_7d": new_7d.scalar() or 0,
        "new_users_30d": new_30d.scalar() or 0,
        "active_buyers_90d": active_buyers.scalar() or 0,
        "role_breakdown": role_breakdown,
    })
