"""
Payments router — 付款 API
POST /payments/create
POST /payments/callback
GET  /payments/:id/status
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.order import Order, OrderStatusLog
from app.models.payment import Payment
from app.schemas.common import SuccessResponse
from app.schemas.order import PaymentCreateRequest

router = APIRouter(prefix="/payments", tags=["付款"])


@router.post("/create", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    data: PaymentCreateRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """建立付款記錄"""
    # Verify order
    result = await db.execute(
        select(Order).where(Order.id == data.order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="訂單不存在")

    if order.payment_status == "paid":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="訂單已付款")

    # Create payment record
    idempotency_key = str(uuid.uuid4())
    payment = Payment(
        order_id=order.id,
        method=data.method,
        amount=float(order.total),
        currency="TWD",
        status="pending",
        idempotency_key=idempotency_key,
    )
    db.add(payment)
    await db.flush()

    # Build payment form data for ECPay / other gateways
    # In production, this would integrate with a real payment gateway
    payment_data = {
        "payment_id": payment.id,
        "order_number": order.order_number,
        "amount": float(order.total),
        "method": data.method,
        "idempotency_key": idempotency_key,
        # ECPay specific fields would be generated here
        "gateway_url": "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5",
    }

    return SuccessResponse(data=payment_data, message="付款建立成功")


@router.post("/callback", response_model=SuccessResponse)
async def payment_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """付款回調（支付閘道通知）"""
    # Parse callback data - ECPay sends form data
    form_data = await request.form()
    data = dict(form_data)

    # In production: verify MAC value from ECPay
    # mac_value = data.get("CheckMacValue")
    # verify_ecpay_mac(data, mac_value)

    merchant_trade_no = data.get("MerchantTradeNo", "")
    rtn_code = data.get("RtnCode", "")
    trade_no = data.get("TradeNo", "")

    # Find order by merchant trade number
    result = await db.execute(
        select(Order).where(Order.order_number == merchant_trade_no)
    )
    order = result.scalar_one_or_none()
    if not order:
        return SuccessResponse(data={"message": "0|OrderNotFound"})

    # Find payment
    payment_result = await db.execute(
        select(Payment).where(Payment.order_id == order.id).order_by(Payment.created_at.desc())
    )
    payment = payment_result.scalar_one_or_none()

    if rtn_code == "1":
        # Payment successful
        if payment:
            payment.status = "completed"
            payment.transaction_id = trade_no
            payment.gateway_response = data

        order.payment_status = "paid"
        old_status = order.status
        order.status = "confirmed"
        db.add(OrderStatusLog(
            order_id=order.id,
            from_status=old_status,
            to_status="confirmed",
            note=f"付款成功 (交易編號: {trade_no})",
        ))
    else:
        # Payment failed
        if payment:
            payment.status = "failed"
            payment.gateway_response = data

        order.payment_status = "failed"

    return SuccessResponse(data={"message": "1|OK"})


@router.get("/{payment_id}/status", response_model=SuccessResponse)
async def get_payment_status(
    payment_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """查詢付款狀態"""
    result = await db.execute(
        select(Payment)
        .join(Order, Payment.order_id == Order.id)
        .where(Payment.id == payment_id, Order.user_id == current_user.id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="付款記錄不存在")

    return SuccessResponse(data={
        "id": payment.id,
        "order_id": payment.order_id,
        "method": payment.method,
        "amount": float(payment.amount),
        "status": payment.status,
        "transaction_id": payment.transaction_id,
        "created_at": payment.created_at.isoformat(),
    })
