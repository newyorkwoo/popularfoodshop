"""
Admin Products router — 商品管理 API
GET    /admin/products
POST   /admin/products
GET    /admin/products/:id
PUT    /admin/products/:id
DELETE /admin/products/:id
POST   /admin/products/:id/images
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.admin_dependencies import get_current_admin_user, require_admin_permission
from app.models.product import Product, ProductImage, ProductVariant
from app.schemas.common import SuccessResponse
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.helpers import generate_slug
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin/products", tags=["管理後台 - 商品"])


@router.get("", response_model=SuccessResponse)
async def list_products(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    _=Depends(require_admin_permission("products.read")),
    db: AsyncSession = Depends(get_db),
):
    """列出所有商品（含搜尋篩選）"""
    query = select(Product).options(
        selectinload(Product.brand),
        selectinload(Product.category),
        selectinload(Product.images),
    )

    if q:
        search_term = f"%{q}%"
        query = query.where(
            or_(Product.name.ilike(search_term), Product.sku.ilike(search_term))
        )
    if category_id:
        query = query.where(Product.category_id == category_id)
    if brand_id:
        query = query.where(Product.brand_id == brand_id)
    if is_active is not None:
        query = query.where(Product.is_active == is_active)

    query = query.order_by(Product.created_at.desc())
    items, meta = await paginate(db, query, page, per_page)

    data = [
        {
            "id": p.id,
            "name": p.name,
            "slug": p.slug,
            "sku": p.sku,
            "price": float(p.price),
            "sale_price": float(p.sale_price) if p.sale_price else None,
            "stock": p.stock,
            "sold_count": p.sold_count,
            "is_active": p.is_active,
            "is_new": p.is_new,
            "is_featured": p.is_featured,
            "brand_name": p.brand.name if p.brand else None,
            "category_name": p.category.name if p.category else None,
            "primary_image": p.primary_image,
            "created_at": p.created_at.isoformat(),
        }
        for p in items
    ]

    return SuccessResponse(data=data, meta=meta)


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    _=Depends(require_admin_permission("products.write")),
    db: AsyncSession = Depends(get_db),
):
    """新增商品"""
    # Check slug uniqueness
    slug = generate_slug(data.name)
    existing = await db.execute(select(Product).where(Product.slug == slug))
    if existing.scalar_one_or_none():
        slug = f"{slug}-{generate_slug(str(data.sku or ''))}"

    product = Product(
        name=data.name,
        slug=slug,
        description=data.description,
        short_description=data.short_description,
        price=data.price,
        sale_price=data.sale_price,
        sku=data.sku,
        barcode=data.barcode,
        stock=data.stock or 0,
        weight=data.weight,
        unit=data.unit,
        origin=data.origin,
        shelf_life=data.shelf_life,
        storage=data.storage,
        allergens=data.allergens,
        nutrition_info=data.nutrition_info,
        tags=data.tags or [],
        meta_title=data.meta_title,
        meta_description=data.meta_description,
        brand_id=data.brand_id,
        category_id=data.category_id,
        is_active=data.is_active if data.is_active is not None else True,
        is_new=data.is_new or False,
        is_featured=data.is_featured or False,
    )
    db.add(product)
    await db.flush()

    # Add images
    if data.images:
        for i, img in enumerate(data.images):
            db.add(ProductImage(
                product_id=product.id,
                url=img.url,
                alt_text=img.alt_text,
                sort_order=img.sort_order or i,
            ))

    # Add variants
    if data.variants:
        for v in data.variants:
            db.add(ProductVariant(
                product_id=product.id,
                name=v.name,
                sku=v.sku,
                price_adjustment=v.price_adjustment or 0,
                stock=v.stock or 0,
                is_active=v.is_active if v.is_active is not None else True,
            ))

    return SuccessResponse(data={"id": product.id, "slug": product.slug}, message="商品已建立")


@router.get("/{product_id}", response_model=SuccessResponse)
async def get_product(
    product_id: int,
    _=Depends(require_admin_permission("products.read")),
    db: AsyncSession = Depends(get_db),
):
    """取得商品詳情"""
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
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

    return SuccessResponse(data={
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "short_description": product.short_description,
        "price": float(product.price),
        "sale_price": float(product.sale_price) if product.sale_price else None,
        "sku": product.sku,
        "barcode": product.barcode,
        "stock": product.stock,
        "weight": float(product.weight) if product.weight else None,
        "unit": product.unit,
        "origin": product.origin,
        "shelf_life": product.shelf_life,
        "storage": product.storage,
        "allergens": product.allergens,
        "nutrition_info": product.nutrition_info,
        "tags": product.tags,
        "meta_title": product.meta_title,
        "meta_description": product.meta_description,
        "brand_id": product.brand_id,
        "brand_name": product.brand.name if product.brand else None,
        "category_id": product.category_id,
        "category_name": product.category.name if product.category else None,
        "is_active": product.is_active,
        "is_new": product.is_new,
        "is_featured": product.is_featured,
        "avg_rating": product.avg_rating,
        "review_count": product.review_count,
        "view_count": product.view_count,
        "sold_count": product.sold_count,
        "images": [
            {"id": img.id, "url": img.url, "alt_text": img.alt_text, "sort_order": img.sort_order}
            for img in product.images
        ],
        "variants": [
            {"id": v.id, "name": v.name, "sku": v.sku, "price_adjustment": float(v.price_adjustment), "stock": v.stock, "is_active": v.is_active}
            for v in product.variants
        ],
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    })


@router.put("/{product_id}", response_model=SuccessResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    _=Depends(require_admin_permission("products.write")),
    db: AsyncSession = Depends(get_db),
):
    """更新商品"""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    update_data = data.model_dump(exclude_unset=True)

    # Update slug if name changed
    if "name" in update_data:
        update_data["slug"] = generate_slug(update_data["name"])

    for field, value in update_data.items():
        if field not in ("images", "variants"):
            setattr(product, field, value)

    return SuccessResponse(data={"id": product.id}, message="商品已更新")


@router.delete("/{product_id}", response_model=SuccessResponse)
async def delete_product(
    product_id: int,
    _=Depends(require_admin_permission("products.delete")),
    db: AsyncSession = Depends(get_db),
):
    """刪除商品（軟刪除）"""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    product.is_active = False
    return SuccessResponse(data={"message": "商品已停用"})
