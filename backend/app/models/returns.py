"""
Return request model — 退貨申請
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


RETURN_STATUS = SAEnum(
    "pending", "approved", "rejected", "shipped", "received", "refunded", "completed",
    name="return_status",
)


class ReturnRequest(Base):
    __tablename__ = "return_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reason: Mapped[str] = mapped_column(String(30), nullable=False)  # defective / wrong_item / changed_mind
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    images: Mapped[list | None] = mapped_column(JSONB, nullable=True)  # 退貨照片 URLs
    status: Mapped[str] = mapped_column(RETURN_STATUS, default="pending", server_default="pending")
    items: Mapped[list | None] = mapped_column(JSONB, nullable=True)  # 退貨商品明細
    refund_amount: Mapped[float | None] = mapped_column(Integer, nullable=True)
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    order = relationship("Order", back_populates="return_requests")

    def __repr__(self):
        return f"<ReturnRequest(id={self.id}, order={self.order_id}, status='{self.status}')>"
