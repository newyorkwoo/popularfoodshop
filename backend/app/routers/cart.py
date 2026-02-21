"""
Cart router — 購物車 API
GET    /cart
POST   /cart/items
PUT    /cart/items/:id
DELETE /cart/items/:id
POST   /cart/coupon
DELETE /cart/coupon
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.cart import CartItem
from app.models.coupon import Coupon
from app.models.product import Product
from app.schemas.common import SuccessResponse
from app.schemas.order import CartItemAdd, CartItemUpdate, CouponApplyRequest

router = APIRouter(prefix="/cart", tags=["購物車"])


@router.get("", response_model=SuccessResponse)
async def get_cart(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得購物車"""
    result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == current_user.id)
        .options(selectinload(CartItem.product).selectinload(Product.images))
        .order_by(CartItem.created_at.desc())
    )
    items = result.scalars().all()

    cart_items = []
    subtotal = 0
    for item in items:
        product = item.product
        if not product or not product.is_active:
            continue
        price = float(product.sale_price or product.price)
        line_total = price * item.quantity
        subtotal += line_total
        cart_items.append({
            "id": item.id,
            "product_id": product.id,
            "name": product.name,
            "slug": product.slug,
            "image": product.primary_image,
            "price": float(product.price),
            "sale_price": float(product.sale_price) if product.sale_price else None,
            "quantity": item.quantity,
            "variant_id": item.variant_id,
            "stock": product.stock,
            "line_total": line_total,
        })

    return SuccessResponse(data={
        "items": cart_items,
        "item_count": len(cart_items),
        "subtotal": subtotal,
    })


@router.post("/items", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    data: CartItemAdd,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """新增商品到購物車"""
    # Check product
    result = await db.execute(
        select(Product).where(Product.id == data.product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    if product.stock < data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="庫存不足")

    # Check if already in cart
    existing = await db.execute(
        select(CartItem).where(
            CartItem.user_id == current_user.id,
            CartItem.product_id == data.product_id,
            CartItem.variant_id == data.variant_id,
        )
    )
    cart_item = existing.scalar_one_or_none()

    if cart_item:
        cart_item.quantity += data.quantity
        if cart_item.quantity > product.stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="超過庫存數量")
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=data.product_id,
            variant_id=data.variant_id,
            quantity=data.quantity,
        )
        db.add(cart_item)

    return SuccessResponse(data={"message": "已加入購物車"})


@router.put("/items/{item_id}", response_model=SuccessResponse)
async def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新購物車商品數量"""
    result = await db.execute(
        select(CartItem)
        .where(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .options(selectinload(CartItem.product))
    )
    cart_item = result.scalar_one_or_none()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="購物車商品不存在")

    if cart_item.product.stock < data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="庫存不足")

    cart_item.quantity = data.quantity
    return SuccessResponse(data={"message": "已更新數量"})


@router.delete("/items/{item_id}", response_model=SuccessResponse)
async def remove_cart_item(
    item_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """移除購物車商品"""
    result = await db.execute(
        select(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user.id)
    )
    cart_item = result.scalar_one_or_none()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="購物車商品不存在")

    await db.delete(cart_item)
    return SuccessResponse(data={"message": "已移除商品"})


@router.post("/coupon", response_model=SuccessResponse)
async def apply_coupon(
    data: CouponApplyRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """套用優惠券"""
    result = await db.execute(
        select(Coupon).where(Coupon.code == data.code.upper())
    )
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="優惠券不存在")

    if not coupon.is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="優惠券已失效或過期")

    # Calculate cart subtotal
    cart_result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == current_user.id)
        .options(selectinload(CartItem.product))
    )
    items = cart_result.scalars().all()
    subtotal = sum(
        float(item.product.sale_price or item.product.price) * item.quantity
        for item in items if item.product and item.product.is_active
    )

    if coupon.min_order_amount and subtotal < float(coupon.min_order_amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"訂單金額需滿 ${coupon.min_order_amount} 才能使用此優惠券",
        )

    # Calculate discount
    if coupon.discount_type == "percentage":
        discount = subtotal * (float(coupon.discount_value) / 100)
        if coupon.max_discount_amount:
            discount = min(discount, float(coupon.max_discount_amount))
    else:
        discount = float(coupon.discount_value)

    return SuccessResponse(data={
        "code": coupon.code,
        "discount_type": coupon.discount_type,
        "discount_value": float(coupon.discount_value),
        "discount_amount": round(discount, 2),
        "message": f"已套用優惠券 {coupon.code}",
    })
