"""
Admin Dashboard router
GET /admin/dashboard
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.admin_dependencies import get_current_admin_user
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/admin/dashboard", tags=["管理後台 - 儀表板"])


@router.get("", response_model=SuccessResponse)
async def dashboard(
    current_admin=Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """後台儀表板統計"""
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    last_30_days = datetime.utcnow() - timedelta(days=30)

    # Total users
    user_count = await db.execute(select(func.count(User.id)))
    total_users = user_count.scalar() or 0

    # New users (30 days)
    new_user_count = await db.execute(
        select(func.count(User.id)).where(User.created_at >= last_30_days)
    )
    new_users = new_user_count.scalar() or 0

    # Total products
    product_count = await db.execute(
        select(func.count(Product.id)).where(Product.is_active == True)
    )
    total_products = product_count.scalar() or 0

    # Low stock products
    low_stock = await db.execute(
        select(func.count(Product.id)).where(Product.is_active == True, Product.stock <= 10)
    )
    low_stock_count = low_stock.scalar() or 0

    # Orders today
    orders_today_result = await db.execute(
        select(func.count(Order.id)).where(
            func.date(Order.created_at) == today
        )
    )
    orders_today = orders_today_result.scalar() or 0

    # Revenue today
    revenue_today_result = await db.execute(
        select(func.coalesce(func.sum(Order.total), 0)).where(
            func.date(Order.created_at) == today,
            Order.payment_status == "paid",
        )
    )
    revenue_today = float(revenue_today_result.scalar() or 0)

    # Monthly revenue
    monthly_revenue_result = await db.execute(
        select(func.coalesce(func.sum(Order.total), 0)).where(
            Order.created_at >= datetime.combine(month_start, datetime.min.time()),
            Order.payment_status == "paid",
        )
    )
    monthly_revenue = float(monthly_revenue_result.scalar() or 0)

    # Pending orders
    pending_orders_result = await db.execute(
        select(func.count(Order.id)).where(Order.status == "pending")
    )
    pending_orders = pending_orders_result.scalar() or 0

    # Recent orders
    recent_orders_result = await db.execute(
        select(Order).order_by(Order.created_at.desc()).limit(10)
    )
    recent_orders = recent_orders_result.scalars().all()

    # Top selling products
    top_products_result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.sold_count.desc())
        .limit(10)
    )
    top_products = top_products_result.scalars().all()

    return SuccessResponse(data={
        "stats": {
            "total_users": total_users,
            "new_users_30d": new_users,
            "total_products": total_products,
            "low_stock_count": low_stock_count,
            "orders_today": orders_today,
            "revenue_today": revenue_today,
            "monthly_revenue": monthly_revenue,
            "pending_orders": pending_orders,
        },
        "recent_orders": [
            {
                "id": o.id,
                "order_number": o.order_number,
                "status": o.status,
                "total": float(o.total),
                "payment_status": o.payment_status,
                "created_at": o.created_at.isoformat(),
            }
            for o in recent_orders
        ],
        "top_products": [
            {
                "id": p.id,
                "name": p.name,
                "sold_count": p.sold_count,
                "stock": p.stock,
                "price": float(p.price),
            }
            for p in top_products
        ],
    })
