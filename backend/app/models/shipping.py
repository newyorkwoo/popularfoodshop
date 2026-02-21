"""
Shipping method model
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ShippingMethod(Base):
    __tablename__ = "shipping_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)  # home_delivery / convenience_store
    description: Mapped[str | None] = mapped_column(String(300), nullable=True)
    fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0, server_default="0")
    free_threshold: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    estimated_days: Mapped[str | None] = mapped_column(String(20), nullable=True)  # "1-3 天"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<ShippingMethod(code='{self.code}', fee={self.fee})>"
