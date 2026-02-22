"""
Tests for Orders API endpoints:
  POST /api/v1/orders
  GET  /api/v1/orders
  GET  /api/v1/orders/:id
  POST /api/v1/orders/:id/cancel
  POST /api/v1/orders/:id/return
"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem, OrderStatusLog
from app.utils.helpers import generate_order_number

API = "/api/v1"


# ── Create Order ─────────────────────────────────────────────
class TestCreateOrder:
    async def test_create_order_success(
        self, client: AsyncClient, auth_headers, test_cart_item, db: AsyncSession
    ):
        resp = await client.post(f"{API}/orders", headers=auth_headers, json={
            "shipping_address": {
                "recipient_name": "Test User",
                "phone": "0912345678",
                "city": "台北市",
                "district": "信義區",
                "address": "信義路一段1號",
            },
            "payment_method": "credit_card",
        })
        assert resp.status_code == 201
        data = resp.json()["data"]
        assert "order_number" in data
        assert data["order_number"].startswith("PFS")

    async def test_create_order_empty_cart(
        self, client: AsyncClient, auth_headers
    ):
        resp = await client.post(f"{API}/orders", headers=auth_headers, json={
            "shipping_address": {
                "recipient_name": "Test",
                "phone": "0911111111",
                "city": "台北市",
                "district": "中山區",
                "address": "Test Rd",
            },
            "payment_method": "credit_card",
        })
        assert resp.status_code == 400

    async def test_create_order_unauthenticated(self, client: AsyncClient):
        resp = await client.post(f"{API}/orders", json={
            "shipping_address": {
                "recipient_name": "X",
                "phone": "000",
                "city": "X",
                "district": "X",
                "address": "X",
            },
        })
        assert resp.status_code == 401


# ── List Orders ──────────────────────────────────────────────
class TestListOrders:
    async def _create_test_order(self, db: AsyncSession, user):
        """Helper to create an order directly in DB."""
        order = Order(
            user_id=user.id,
            order_number=generate_order_number(),
            status="pending",
            subtotal=1000,
            discount=0,
            shipping_fee=0,
            total=1000,
            payment_method="credit_card",
            payment_status="pending",
            shipping_address={
                "recipient_name": "Test",
                "phone": "0912345678",
                "city": "台北市",
                "district": "信義區",
                "address": "Test Rd",
            },
        )
        db.add(order)
        await db.flush()
        await db.commit()
        await db.refresh(order)
        return order

    async def test_list_orders_empty(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/orders", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)

    async def test_list_orders_with_data(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        await self._create_test_order(db, test_user)
        resp = await client.get(f"{API}/orders", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert len(data) >= 1

    async def test_list_orders_pagination(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        for _ in range(3):
            await self._create_test_order(db, test_user)
        resp = await client.get(
            f"{API}/orders", headers=auth_headers, params={"page": 1, "per_page": 2}
        )
        assert resp.status_code == 200

    async def test_list_orders_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{API}/orders")
        assert resp.status_code == 401


# ── Get Order Detail ─────────────────────────────────────────
class TestGetOrder:
    async def test_get_order_success(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        order = Order(
            user_id=test_user.id,
            order_number=generate_order_number(),
            status="pending",
            subtotal=500,
            discount=0,
            shipping_fee=0,
            total=500,
            payment_method="credit_card",
            payment_status="pending",
            shipping_address={
                "recipient_name": "Test",
                "phone": "0912345678",
                "city": "台北市",
                "district": "信義區",
                "address": "Test Rd",
            },
        )
        db.add(order)
        await db.flush()
        await db.commit()
        await db.refresh(order)

        resp = await client.get(f"{API}/orders/{order.id}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["order_number"] == order.order_number

    async def test_get_order_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/orders/99999", headers=auth_headers)
        assert resp.status_code == 404


# ── Cancel Order ─────────────────────────────────────────────
class TestCancelOrder:
    async def test_cancel_pending_order(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        order = Order(
            user_id=test_user.id,
            order_number=generate_order_number(),
            status="pending",
            subtotal=500,
            discount=0,
            shipping_fee=0,
            total=500,
            payment_method="credit_card",
            payment_status="pending",
            shipping_address={},
        )
        db.add(order)
        await db.flush()
        await db.commit()
        await db.refresh(order)

        resp = await client.post(f"{API}/orders/{order.id}/cancel", headers=auth_headers)
        assert resp.status_code == 200

    async def test_cancel_shipped_order(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        order = Order(
            user_id=test_user.id,
            order_number=generate_order_number(),
            status="shipped",
            subtotal=500,
            discount=0,
            shipping_fee=0,
            total=500,
            payment_method="credit_card",
            payment_status="paid",
            shipping_address={},
        )
        db.add(order)
        await db.flush()
        await db.commit()
        await db.refresh(order)

        resp = await client.post(f"{API}/orders/{order.id}/cancel", headers=auth_headers)
        assert resp.status_code == 400

    async def test_cancel_order_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{API}/orders/99999/cancel", headers=auth_headers)
        assert resp.status_code == 404


# ── Return Request ───────────────────────────────────────────
class TestReturnOrder:
    async def test_return_delivered_order(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        order = Order(
            user_id=test_user.id,
            order_number=generate_order_number(),
            status="delivered",
            subtotal=500,
            discount=0,
            shipping_fee=0,
            total=500,
            payment_method="credit_card",
            payment_status="paid",
            shipping_address={},
        )
        db.add(order)
        await db.flush()
        await db.commit()
        await db.refresh(order)

        resp = await client.post(
            f"{API}/orders/{order.id}/return",
            headers=auth_headers,
            json={"reason": "商品瑕疵"},
        )
        assert resp.status_code == 201

    async def test_return_pending_order(
        self, client: AsyncClient, auth_headers, test_user, db: AsyncSession
    ):
        order = Order(
            user_id=test_user.id,
            order_number=generate_order_number(),
            status="pending",
            subtotal=500,
            discount=0,
            shipping_fee=0,
            total=500,
            payment_method="credit_card",
            payment_status="pending",
            shipping_address={},
        )
        db.add(order)
        await db.flush()
        await db.commit()
        await db.refresh(order)

        resp = await client.post(
            f"{API}/orders/{order.id}/return",
            headers=auth_headers,
            json={"reason": "商品瑕疵"},
        )
        assert resp.status_code == 400
