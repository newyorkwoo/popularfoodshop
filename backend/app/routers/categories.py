"""
Categories router — 分類 API
GET  /categories
GET  /categories/:slug/products
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.common import SuccessResponse
from app.utils.pagination import paginate

router = APIRouter(prefix="/categories", tags=["分類"])


@router.get("", response_model=SuccessResponse)
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    """取得分類樹（含子分類）"""
    result = await db.execute(
        select(Category)
        .where(Category.parent_id == None, Category.is_active == True)
        .options(selectinload(Category.children))
        .order_by(Category.sort_order.asc(), Category.name.asc())
    )
    categories = result.scalars().all()

    def serialize(cat):
        return {
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "description": cat.description,
            "image": cat.image,
            "sort_order": cat.sort_order,
            "children": [
                serialize(child) for child in cat.children if child.is_active
            ],
        }

    data = [serialize(c) for c in categories]
    return SuccessResponse(data=data)


@router.get("/{slug}", response_model=SuccessResponse)
async def get_category(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """取得分類詳情"""
    result = await db.execute(
        select(Category)
        .where(Category.slug == slug, Category.is_active == True)
        .options(selectinload(Category.children))
    )
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分類不存在")

    return SuccessResponse(data={
        "id": cat.id,
        "name": cat.name,
        "slug": cat.slug,
        "description": cat.description,
        "image": cat.image,
        "children": [
            {"id": c.id, "name": c.name, "slug": c.slug}
            for c in cat.children if c.is_active
        ],
    })


@router.get("/{slug}/products", response_model=SuccessResponse)
async def category_products(
    slug: str,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    sort_by: str = Query(default="created_at", regex="^(created_at|price|sold_count|avg_rating)$"),
    sort_order: str = Query(default="desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    """取得分類下的商品"""
    result = await db.execute(
        select(Category).where(Category.slug == slug, Category.is_active == True)
    )
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分類不存在")

    # Include subcategory IDs
    sub_result = await db.execute(
        select(Category.id).where(Category.parent_id == cat.id)
    )
    sub_ids = [row[0] for row in sub_result.all()]
    category_ids = [cat.id] + sub_ids

    query = (
        select(Product)
        .where(Product.is_active == True, Product.category_id.in_(category_ids))
        .options(selectinload(Product.brand), selectinload(Product.images))
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
            "brand_name": item.brand.name if item.brand else None,
            "primary_image": item.primary_image,
            "avg_rating": item.avg_rating,
            "is_new": item.is_new,
            "stock": item.stock,
        })

    return SuccessResponse(
        data={"category": {"id": cat.id, "name": cat.name, "slug": cat.slug}, "products": data},
        meta=meta,
    )
