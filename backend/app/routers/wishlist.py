"""
Wishlist router — 收藏清單 API
GET    /wishlist
POST   /wishlist/:product_id
DELETE /wishlist/:product_id
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.product import Product
from app.models.wishlist import Wishlist
from app.schemas.common import SuccessResponse
from app.utils.pagination import paginate

router = APIRouter(prefix="/wishlist", tags=["收藏"])


@router.get("", response_model=SuccessResponse)
async def get_wishlist(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得收藏清單"""
    query = (
        select(Wishlist)
        .where(Wishlist.user_id == current_user.id)
        .options(
            selectinload(Wishlist.product).selectinload(Product.images),
            selectinload(Wishlist.product).selectinload(Product.brand),
        )
        .order_by(Wishlist.created_at.desc())
    )

    items, meta = await paginate(db, query, page, per_page)

    data = []
    for w in items:
        product = w.product
        if not product:
            continue
        data.append({
            "id": w.id,
            "product_id": product.id,
            "name": product.name,
            "slug": product.slug,
            "price": float(product.price),
            "sale_price": float(product.sale_price) if product.sale_price else None,
            "brand_name": product.brand.name if product.brand else None,
            "primary_image": product.primary_image,
            "is_active": product.is_active,
            "stock": product.stock,
            "added_at": w.created_at.isoformat(),
        })

    return SuccessResponse(data=data, meta=meta)


@router.post("/{product_id}", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    product_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """加入收藏"""
    # Check product exists
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active == True)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    # Check if already in wishlist
    existing = await db.execute(
        select(Wishlist).where(
            Wishlist.user_id == current_user.id,
            Wishlist.product_id == product_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="已在收藏清單中")

    db.add(Wishlist(user_id=current_user.id, product_id=product_id))
    return SuccessResponse(data={"message": "已加入收藏"})


@router.delete("/{product_id}", response_model=SuccessResponse)
async def remove_from_wishlist(
    product_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """移除收藏"""
    result = await db.execute(
        select(Wishlist).where(
            Wishlist.user_id == current_user.id,
            Wishlist.product_id == product_id,
        )
    )
    wishlist_item = result.scalar_one_or_none()
    if not wishlist_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏不存在")

    await db.delete(wishlist_item)
    return SuccessResponse(data={"message": "已移除收藏"})
