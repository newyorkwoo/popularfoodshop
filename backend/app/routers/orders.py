"""
Orders router — 訂單 API
POST /orders
GET  /orders
GET  /orders/:id
POST /orders/:id/cancel
POST /orders/:id/return
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.cart import CartItem
from app.models.coupon import Coupon, CouponUsage
from app.models.order import Order, OrderItem, OrderStatusLog
from app.models.product import Product
from app.models.returns import ReturnRequest
from app.models.shipping import ShippingMethod
from app.models.points import PointsTransaction
from app.schemas.common import SuccessResponse
from app.schemas.order import OrderCreate, ReturnCreate
from app.utils.helpers import generate_order_number
from app.utils.pagination import paginate

router = APIRouter(prefix="/orders", tags=["訂單"])


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """建立訂單"""
    # Get cart items
    cart_result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == current_user.id)
        .options(selectinload(CartItem.product))
    )
    cart_items = cart_result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="購物車是空的")

    # Calculate subtotal and validate stock
    subtotal = 0
    order_items = []
    for ci in cart_items:
        product = ci.product
        if not product or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"商品 {product.name if product else '未知'} 已下架",
            )
        if product.stock < ci.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"商品 {product.name} 庫存不足",
            )
        unit_price = float(product.sale_price or product.price)
        line_total = unit_price * ci.quantity
        subtotal += line_total
        order_items.append({
            "product": product,
            "quantity": ci.quantity,
            "variant_id": ci.variant_id,
            "unit_price": unit_price,
            "total_price": line_total,
        })

    # Coupon discount
    discount = 0
    coupon_code = None
    if data.coupon_code:
        result = await db.execute(
            select(Coupon).where(Coupon.code == data.coupon_code.upper())
        )
        coupon = result.scalar_one_or_none()
        if coupon and coupon.is_valid:
            coupon_code = coupon.code
            if coupon.discount_type == "percentage":
                discount = subtotal * (float(coupon.discount_value) / 100)
                if coupon.max_discount_amount:
                    discount = min(discount, float(coupon.max_discount_amount))
            else:
                discount = float(coupon.discount_value)
            coupon.used_count += 1
            db.add(CouponUsage(coupon_id=coupon.id, user_id=current_user.id))

    # Points
    points_used = 0
    points_discount = 0
    if data.points_used and data.points_used > 0:
        if current_user.points < data.points_used:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="點數不足")
        points_used = data.points_used
        points_discount = points_used  # 1 point = NT$1
        current_user.points -= points_used
        db.add(PointsTransaction(
            user_id=current_user.id,
            type="redeem",
            amount=-points_used,
            description="訂單折抵",
        ))

    # Credits
    credits_used = 0
    if data.credits_used and data.credits_used > 0:
        if current_user.credits < data.credits_used:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="購物金不足")
        credits_used = data.credits_used
        current_user.credits -= credits_used

    # Shipping
    shipping_fee = 0
    if data.shipping_method_id:
        sm_result = await db.execute(
            select(ShippingMethod).where(ShippingMethod.id == data.shipping_method_id)
        )
        shipping_method = sm_result.scalar_one_or_none()
        if shipping_method:
            shipping_fee = float(shipping_method.fee)
            if shipping_method.free_threshold and subtotal >= float(shipping_method.free_threshold):
                shipping_fee = 0

    total = subtotal - discount - points_discount - credits_used + shipping_fee
    if total < 0:
        total = 0

    # Create order
    order = Order(
        user_id=current_user.id,
        order_number=generate_order_number(),
        status="pending",
        subtotal=subtotal,
        discount=discount,
        shipping_fee=shipping_fee,
        total=round(total, 2),
        points_used=points_used,
        credits_used=credits_used,
        coupon_code=coupon_code,
        payment_method=data.payment_method,
        shipping_address={
            "recipient_name": data.shipping_address.recipient_name,
            "phone": data.shipping_address.phone,
            "zip_code": data.shipping_address.zip_code,
            "city": data.shipping_address.city,
            "district": data.shipping_address.district,
            "address": data.shipping_address.address,
        },
        note=data.note,
    )
    db.add(order)
    await db.flush()

    # Create order items + update stock
    for oi in order_items:
        product = oi["product"]
        db.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            variant_id=oi["variant_id"],
            product_name=product.name,
            product_image=product.primary_image,
            product_sku=product.sku,
            unit_price=oi["unit_price"],
            quantity=oi["quantity"],
            total_price=oi["total_price"],
        ))
        product.stock -= oi["quantity"]
        product.sold_count += oi["quantity"]

    # Status log
    db.add(OrderStatusLog(
        order_id=order.id,
        from_status="",
        to_status="pending",
        note="訂單已建立",
    ))

    # Clear cart
    for ci in cart_items:
        await db.delete(ci)

    return SuccessResponse(
        data={"order_id": order.id, "order_number": order.order_number, "total": float(order.total)},
        message="訂單已建立",
    )


@router.get("", response_model=SuccessResponse)
async def list_orders(
    status_filter: str = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=50),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得我的訂單列表"""
    query = (
        select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    if status_filter:
        query = query.where(Order.status == status_filter)

    items, meta = await paginate(db, query, page, per_page)

    data = []
    for order in items:
        data.append({
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total": float(order.total),
            "payment_method": order.payment_method,
            "payment_status": order.payment_status,
            "created_at": order.created_at.isoformat(),
        })

    return SuccessResponse(data=data, meta=meta)


@router.get("/{order_id}", response_model=SuccessResponse)
async def get_order(
    order_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得訂單詳情"""
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id, Order.user_id == current_user.id)
        .options(
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


@router.post("/{order_id}/cancel", response_model=SuccessResponse)
async def cancel_order(
    order_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取消訂單"""
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id, Order.user_id == current_user.id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="訂單不存在")

    if order.status not in ("pending", "confirmed"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="此訂單無法取消")

    old_status = order.status
    order.status = "cancelled"

    # Restore stock
    for oi in order.items:
        prod_result = await db.execute(select(Product).where(Product.id == oi.product_id))
        product = prod_result.scalar_one_or_none()
        if product:
            product.stock += oi.quantity
            product.sold_count -= oi.quantity

    # Restore points / credits
    if order.points_used > 0:
        current_user.points += order.points_used
        db.add(PointsTransaction(
            user_id=current_user.id,
            type="adjust",
            amount=order.points_used,
            description=f"訂單取消退還 ({order.order_number})",
        ))
    if order.credits_used > 0:
        current_user.credits += float(order.credits_used)

    db.add(OrderStatusLog(
        order_id=order.id,
        from_status=old_status,
        to_status="cancelled",
        note="會員取消訂單",
    ))

    return SuccessResponse(data={"message": "訂單已取消"})


@router.post("/{order_id}/return", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_return(
    order_id: int,
    data: ReturnCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """申請退貨"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="訂單不存在")

    if order.status != "delivered":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="僅已送達的訂單可申請退貨")

    # Check existing return
    existing = await db.execute(
        select(ReturnRequest).where(
            ReturnRequest.order_id == order_id,
            ReturnRequest.status.in_(["pending", "approved"]),
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="已有進行中的退貨申請")

    return_request = ReturnRequest(
        order_id=order.id,
        user_id=current_user.id,
        reason=data.reason,
        description=data.description,
        images=data.images or [],
        refund_amount=float(order.total),
    )
    db.add(return_request)

    order.status = "return_requested"
    db.add(OrderStatusLog(
        order_id=order.id,
        from_status="delivered",
        to_status="return_requested",
        note=f"退貨原因: {data.reason}",
    ))

    return SuccessResponse(data={"message": "退貨申請已送出"})
