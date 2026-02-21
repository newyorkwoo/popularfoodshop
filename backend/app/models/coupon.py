"""
Coupon models — coupons, coupon_usages
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    discount_type: Mapped[str] = mapped_column(
        SAEnum("percentage", "fixed", name="discount_type"), nullable=False
    )  # percentage / fixed
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    min_order_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0, server_default="0")
    max_discount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)  # 最高折抵金額
    usage_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 總使用次數上限
    usage_per_user: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    used_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    applicable_products: Mapped[list | None] = mapped_column(JSONB, nullable=True)  # 限定商品 IDs
    applicable_categories: Mapped[list | None] = mapped_column(JSONB, nullable=True)  # 限定分類 IDs
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    usages = relationship("CouponUsage", back_populates="coupon", cascade="all, delete-orphan")

    @property
    def is_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        return (
            self.is_active
            and self.starts_at <= now <= self.expires_at
            and (self.usage_limit is None or self.used_count < self.usage_limit)
        )

    def __repr__(self):
        return f"<Coupon(code='{self.code}', type='{self.discount_type}')>"


class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    coupon_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    order_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True
    )
    discount_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    coupon = relationship("Coupon", back_populates="usages")

    def __repr__(self):
        return f"<CouponUsage(coupon={self.coupon_id}, user={self.user_id})>"
