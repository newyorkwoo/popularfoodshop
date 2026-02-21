"""
Products router — 商品 API
GET  /products
GET  /products/search
GET  /products/trending
GET  /products/:id
GET  /products/:id/reviews
POST /products/:id/reviews
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import get_current_user, get_current_user_optional
from app.models.product import Product, ProductReview
from app.models.brand import Brand
from app.models.category import Category
from app.schemas.common import PaginationMeta, SuccessResponse
from app.schemas.product import (
    ProductDetailResponse,
    ProductListResponse,
    ReviewCreate,
    ReviewResponse,
)
from app.utils.pagination import paginate

router = APIRouter(prefix="/products", tags=["商品"])


@router.get("", response_model=SuccessResponse)
async def list_products(
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_new: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    tags: Optional[str] = None,
    sort_by: str = Query(default="created_at", regex="^(created_at|price|sold_count|avg_rating|name)$"),
    sort_order: str = Query(default="desc", regex="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """取得商品列表（分頁、篩選、排序）"""
    query = select(Product).where(Product.is_active == True)

    # Filters
    if category_id:
        query = query.where(Product.category_id == category_id)
    if brand_id:
        query = query.where(Product.brand_id == brand_id)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if is_new is not None:
        query = query.where(Product.is_new == is_new)
    if is_featured is not None:
        query = query.where(Product.is_featured == is_featured)

    # Sort
    sort_column = getattr(Product, sort_by, Product.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Eager load relationships
    query = query.options(
        selectinload(Product.brand),
        selectinload(Product.category),
        selectinload(Product.images),
    )

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
            "category_name": item.category.name if item.category else None,
            "primary_image": item.primary_image,
            "avg_rating": item.avg_rating,
            "review_count": item.review_count,
            "is_new": item.is_new,
            "is_featured": item.is_featured,
            "stock": item.stock,
        })

    return SuccessResponse(data=data, meta=meta)


@router.get("/search", response_model=SuccessResponse)
async def search_products(
    q: str = Query(min_length=1, max_length=100),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """搜尋商品"""
    search_term = f"%{q}%"
    query = (
        select(Product)
        .where(
            Product.is_active == True,
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.tags.contains([q]),
            ),
        )
        .options(
            selectinload(Product.brand),
            selectinload(Product.images),
        )
        .order_by(Product.sold_count.desc())
    )

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
            "review_count": item.review_count,
            "is_new": item.is_new,
            "stock": item.stock,
        })

    return SuccessResponse(data=data, meta=meta)


@router.get("/trending", response_model=SuccessResponse)
async def trending_products(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """取得熱門商品"""
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .options(selectinload(Product.brand), selectinload(Product.images))
        .order_by(Product.sold_count.desc())
        .limit(limit)
    )
    items = result.scalars().all()

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
            "sold_count": item.sold_count,
        })

    return SuccessResponse(data=data)


@router.get("/{product_id}", response_model=SuccessResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    """取得商品詳情"""
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id, Product.is_active == True)
        .options(
            selectinload(Product.brand),
            selectinload(Product.category),
            selectinload(Product.images),
            selectinload(Product.variants),
        )
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    # Increment view count
    product.view_count += 1

    data = ProductDetailResponse(
        id=product.id,
        name=product.name,
        slug=product.slug,
        description=product.description,
        short_description=product.short_description,
        price=float(product.price),
        sale_price=float(product.sale_price) if product.sale_price else None,
        sku=product.sku,
        barcode=product.barcode,
        stock=product.stock,
        weight=float(product.weight) if product.weight else None,
        unit=product.unit,
        origin=product.origin,
        shelf_life=product.shelf_life,
        storage=product.storage,
        allergens=product.allergens,
        nutrition_info=product.nutrition_info,
        tags=product.tags,
        brand_id=product.brand_id,
        brand_name=product.brand.name if product.brand else None,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None,
        is_new=product.is_new,
        is_featured=product.is_featured,
        is_active=product.is_active,
        avg_rating=product.avg_rating,
        review_count=product.review_count,
        view_count=product.view_count,
        sold_count=product.sold_count,
        images=[{"id": img.id, "url": img.url, "alt_text": img.alt_text, "sort_order": img.sort_order} for img in product.images],
        variants=[{"id": v.id, "name": v.name, "sku": v.sku, "price_adjustment": float(v.price_adjustment), "stock": v.stock, "is_active": v.is_active} for v in product.variants],
        created_at=product.created_at,
    )

    return SuccessResponse(data=data.model_dump())


@router.get("/{product_id}/reviews", response_model=SuccessResponse)
async def list_reviews(
    product_id: int,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """取得商品評價"""
    query = (
        select(ProductReview)
        .where(ProductReview.product_id == product_id, ProductReview.is_visible == True)
        .order_by(ProductReview.created_at.desc())
    )

    items, meta = await paginate(db, query, page, per_page)

    data = []
    for review in items:
        data.append({
            "id": review.id,
            "user_id": review.user_id,
            "rating": review.rating,
            "title": review.title,
            "content": review.content,
            "is_verified": review.is_verified,
            "created_at": review.created_at.isoformat(),
        })

    return SuccessResponse(data=data, meta=meta)


@router.post("/{product_id}/reviews", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    product_id: int,
    data: ReviewCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """新增商品評價"""
    # Check product exists
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    # Check if already reviewed
    existing = await db.execute(
        select(ProductReview).where(
            ProductReview.product_id == product_id,
            ProductReview.user_id == current_user.id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="您已評價過此商品")

    review = ProductReview(
        product_id=product_id,
        user_id=current_user.id,
        rating=data.rating,
        title=data.title,
        content=data.content,
    )
    db.add(review)
    await db.flush()

    # Update product avg rating
    rating_result = await db.execute(
        select(
            func.avg(ProductReview.rating),
            func.count(ProductReview.id),
        ).where(ProductReview.product_id == product_id)
    )
    avg, count = rating_result.one()
    product.avg_rating = float(avg) if avg else 0
    product.review_count = count

    return SuccessResponse(
        data=ReviewResponse.model_validate(review).model_dump(),
        message="評價已送出",
    )
