"""
Product schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ===== Product Schemas =====

class ProductImageResponse(BaseModel):
    id: int
    url: str
    alt_text: Optional[str] = None
    sort_order: int = 0

    class Config:
        from_attributes = True


class ProductVariantResponse(BaseModel):
    id: int
    name: str
    sku: Optional[str] = None
    price_adjustment: float = 0
    stock: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """商品列表回應（簡要）"""
    id: int
    name: str
    slug: str
    price: float
    sale_price: Optional[float] = None
    brand_name: Optional[str] = None
    category_name: Optional[str] = None
    primary_image: Optional[str] = None
    avg_rating: float = 0
    review_count: int = 0
    is_new: bool = False
    is_featured: bool = False
    stock: int = 0

    class Config:
        from_attributes = True


class ProductDetailResponse(BaseModel):
    """商品詳情回應（完整）"""
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: float
    sale_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    stock: int = 0
    weight: Optional[float] = None
    unit: Optional[str] = None
    origin: Optional[str] = None
    shelf_life: Optional[str] = None
    storage: Optional[str] = None
    allergens: Optional[str] = None
    nutrition_info: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    brand_id: Optional[int] = None
    brand_name: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    is_new: bool = False
    is_featured: bool = False
    is_active: bool = True
    avg_rating: float = 0
    review_count: int = 0
    view_count: int = 0
    sold_count: int = 0
    images: List[ProductImageResponse] = []
    variants: List[ProductVariantResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    """新增商品"""
    name: str = Field(max_length=255)
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    sale_price: Optional[float] = Field(default=None, ge=0)
    sku: Optional[str] = Field(default=None, max_length=50)
    barcode: Optional[str] = Field(default=None, max_length=50)
    stock: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)
    weight: Optional[float] = None
    unit: Optional[str] = None
    origin: Optional[str] = None
    shelf_life: Optional[str] = None
    storage: Optional[str] = None
    allergens: Optional[str] = None
    nutrition_info: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    is_active: bool = True
    is_new: bool = False
    is_featured: bool = False


class ProductUpdate(BaseModel):
    """更新商品"""
    name: Optional[str] = Field(default=None, max_length=255)
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    sale_price: Optional[float] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    stock: Optional[int] = Field(default=None, ge=0)
    low_stock_threshold: Optional[int] = None
    weight: Optional[float] = None
    unit: Optional[str] = None
    origin: Optional[str] = None
    shelf_life: Optional[str] = None
    storage: Optional[str] = None
    allergens: Optional[str] = None
    nutrition_info: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_new: Optional[bool] = None
    is_featured: Optional[bool] = None


# ===== Review Schemas =====

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    title: Optional[str] = Field(default=None, max_length=200)
    content: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    user_name: Optional[str] = None
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None
    is_verified: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Category Schemas =====

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True
    sort_order: int = 0
    product_count: int = 0
    children: List["CategoryResponse"] = []

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    slug: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    slug: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


# ===== Brand Schemas =====

class BrandResponse(BaseModel):
    id: int
    name: str
    slug: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True
    product_count: int = 0

    class Config:
        from_attributes = True


class BrandCreate(BaseModel):
    name: str = Field(max_length=100)
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True


class BrandUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
