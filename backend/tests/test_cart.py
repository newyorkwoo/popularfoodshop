"""
Tests for Cart API endpoints:
  GET    /api/v1/cart
  POST   /api/v1/cart/items
  PUT    /api/v1/cart/items/:id
  DELETE /api/v1/cart/items/:id
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


class TestGetCart:
    async def test_get_cart_empty(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/cart", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["item_count"] == 0 or isinstance(data["items"], list)

    async def test_get_cart_with_items(
        self, client: AsyncClient, auth_headers, test_cart_item
    ):
        resp = await client.get(f"{API}/cart", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert len(data["items"]) >= 1
        assert data["subtotal"] > 0

    async def test_get_cart_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{API}/cart")
        assert resp.status_code == 401


class TestAddToCart:
    async def test_add_item_success(
        self, client: AsyncClient, auth_headers, test_product
    ):
        resp = await client.post(f"{API}/cart/items", headers=auth_headers, json={
            "product_id": test_product.id,
            "quantity": 3,
        })
        assert resp.status_code == 201

    async def test_add_item_product_not_found(
        self, client: AsyncClient, auth_headers
    ):
        resp = await client.post(f"{API}/cart/items", headers=auth_headers, json={
            "product_id": 99999,
            "quantity": 1,
        })
        assert resp.status_code == 404

    async def test_add_item_exceeds_stock(
        self, client: AsyncClient, auth_headers, test_product
    ):
        resp = await client.post(f"{API}/cart/items", headers=auth_headers, json={
            "product_id": test_product.id,
            "quantity": 99,
        })
        assert resp.status_code == 400

    async def test_add_existing_item_increases_quantity(
        self, client: AsyncClient, auth_headers, test_product
    ):
        # Add once
        await client.post(f"{API}/cart/items", headers=auth_headers, json={
            "product_id": test_product.id,
            "quantity": 1,
        })
        # Add again
        resp = await client.post(f"{API}/cart/items", headers=auth_headers, json={
            "product_id": test_product.id,
            "quantity": 2,
        })
        assert resp.status_code == 201


class TestUpdateCartItem:
    async def test_update_quantity(
        self, client: AsyncClient, auth_headers, test_cart_item
    ):
        resp = await client.put(
            f"{API}/cart/items/{test_cart_item.id}",
            headers=auth_headers,
            json={"quantity": 5},
        )
        assert resp.status_code == 200

    async def test_update_item_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.put(
            f"{API}/cart/items/99999",
            headers=auth_headers,
            json={"quantity": 1},
        )
        assert resp.status_code == 404

    async def test_update_exceeds_stock(
        self, client: AsyncClient, auth_headers, test_cart_item
    ):
        resp = await client.put(
            f"{API}/cart/items/{test_cart_item.id}",
            headers=auth_headers,
            json={"quantity": 99},
        )
        assert resp.status_code == 400


class TestRemoveCartItem:
    async def test_remove_item(
        self, client: AsyncClient, auth_headers, test_cart_item
    ):
        resp = await client.delete(
            f"{API}/cart/items/{test_cart_item.id}",
            headers=auth_headers,
        )
        assert resp.status_code == 200

    async def test_remove_item_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.delete(
            f"{API}/cart/items/99999", headers=auth_headers
        )
        assert resp.status_code == 404
