"""
Brands router — 品牌 API
GET  /brands
GET  /brands/:slug
GET  /brands/:slug/products
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.brand import Brand
from app.models.product import Product
from app.schemas.common import SuccessResponse
from app.utils.pagination import paginate

router = APIRouter(prefix="/brands", tags=["品牌"])


@router.get("", response_model=SuccessResponse)
async def list_brands(
    db: AsyncSession = Depends(get_db),
):
    """取得所有品牌"""
    result = await db.execute(
        select(Brand)
        .where(Brand.is_active == True)
        .order_by(Brand.sort_order.asc(), Brand.name.asc())
    )
    brands = result.scalars().all()

    data = [
        {
            "id": b.id,
            "name": b.name,
            "slug": b.slug,
            "logo": b.logo_url,
            "description": b.description,
            "country": b.country,
        }
        for b in brands
    ]
    return SuccessResponse(data=data)


@router.get("/{slug}", response_model=SuccessResponse)
async def get_brand(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """取得品牌詳情"""
    result = await db.execute(
        select(Brand).where(Brand.slug == slug, Brand.is_active == True)
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="品牌不存在")

    return SuccessResponse(data={
        "id": brand.id,
        "name": brand.name,
        "slug": brand.slug,
        "logo": brand.logo_url,
        "description": brand.description,
        "website": brand.website_url,
        "country": brand.country,
    })


@router.get("/{slug}/products", response_model=SuccessResponse)
async def brand_products(
    slug: str,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    sort_by: str = Query(default="created_at", regex="^(created_at|price|sold_count|avg_rating)$"),
    sort_order: str = Query(default="desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    """取得品牌下的商品"""
    result = await db.execute(
        select(Brand).where(Brand.slug == slug, Brand.is_active == True)
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="品牌不存在")

    query = (
        select(Product)
        .where(Product.is_active == True, Product.brand_id == brand.id)
        .options(selectinload(Product.images), selectinload(Product.category))
    )

    sort_column = getattr(Product, sort_by, Product.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    items, meta = await paginate(db, query, page, per_page)

    data = []
    for item in items:
        data.append({
            "id": item.id,
            "name": item.name,
            "slug": item.slug,
            "price": float(item.price),
            "sale_price": float(item.sale_price) if item.sale_price else None,
            "category_name": item.category.name if item.category else None,
            "primary_image": item.primary_image,
            "avg_rating": item.avg_rating,
            "is_new": item.is_new,
            "stock": item.stock,
        })

    return SuccessResponse(
        data={"brand": {"id": brand.id, "name": brand.name, "slug": brand.slug, "logo": brand.logo_url}, "products": data},
        meta=meta,
    )
