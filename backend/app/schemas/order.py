"""
Order schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ===== Cart Schemas =====

class CartItemAdd(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(default=1, ge=1, le=99)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, le=99)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    variant_id: Optional[int] = None
    variant_name: Optional[str] = None
    unit_price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: List[CartItemResponse] = []
    item_count: int = 0
    subtotal: float = 0
    discount: float = 0
    shipping_fee: float = 0
    total: float = 0
    coupon_code: Optional[str] = None


class CouponApplyRequest(BaseModel):
    code: str = Field(max_length=50)


# ===== Order Schemas =====

class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int] = None
    product_name: str
    product_image: Optional[str] = None
    variant_name: Optional[str] = None
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class ShippingAddress(BaseModel):
    recipient_name: str
    phone: str
    zip_code: Optional[str] = None
    city: str
    district: str
    address: str


class OrderCreate(BaseModel):
    shipping_address: ShippingAddress
    shipping_method: str = Field(default="home_delivery")
    payment_method: str = Field(default="credit_card")
    coupon_code: Optional[str] = None
    points_used: int = Field(default=0, ge=0)
    credits_used: int = Field(default=0, ge=0)
    customer_notes: Optional[str] = None


class OrderListResponse(BaseModel):
    id: int
    order_number: str
    status: str
    total: float
    item_count: int = 0
    first_item_name: Optional[str] = None
    first_item_image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderDetailResponse(BaseModel):
    id: int
    order_number: str
    status: str
    payment_status: str
    payment_method: Optional[str] = None
    subtotal: float
    discount: float = 0
    shipping_fee: float = 0
    total: float
    points_used: int = 0
    credits_used: int = 0
    coupon_code: Optional[str] = None
    shipping_method: Optional[str] = None
    shipping_address: Optional[Dict[str, Any]] = None
    tracking_number: Optional[str] = None
    customer_notes: Optional[str] = None
    items: List[OrderItemResponse] = []
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """管理員更新訂單狀態"""
    status: str
    tracking_number: Optional[str] = None
    admin_notes: Optional[str] = None


# ===== Return Schemas =====

class ReturnCreate(BaseModel):
    reason: str
    description: Optional[str] = None
    images: Optional[List[str]] = None  # 退貨照片 URLs
    items: Optional[List[Dict[str, Any]]] = None  # [{product_id, quantity}]


class ReturnResponse(BaseModel):
    id: int
    order_id: int
    order_number: Optional[str] = None
    reason: str
    description: Optional[str] = None
    status: str
    refund_amount: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Payment Schemas =====

class PaymentCreateRequest(BaseModel):
    order_id: int
    payment_method: str
    idempotency_key: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    payment_method: str
    amount: float
    status: str
    transaction_id: Optional[str] = None
    payment_url: Optional[str] = None  # 第三方支付導向 URL
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Coupon Schemas =====

class CouponResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    discount_type: str
    discount_value: float
    min_order_amount: float = 0
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    used_count: int = 0
    is_active: bool = True
    starts_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


class CouponCreate(BaseModel):
    code: str = Field(max_length=50)
    name: str = Field(max_length=100)
    description: Optional[str] = None
    discount_type: str  # percentage / fixed
    discount_value: float = Field(gt=0)
    min_order_amount: float = Field(default=0, ge=0)
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_per_user: int = Field(default=1, ge=1)
    starts_at: datetime
    expires_at: datetime
    is_active: bool = True


class CouponUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    discount_value: Optional[float] = None
    min_order_amount: Optional[float] = None
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    is_active: Optional[bool] = None
    starts_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
