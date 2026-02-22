"""
Tests for Wishlist API endpoints:
  GET    /api/v1/wishlist
  POST   /api/v1/wishlist/:product_id
  DELETE /api/v1/wishlist/:product_id
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


class TestGetWishlist:
    async def test_get_wishlist_empty(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/wishlist", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)

    async def test_get_wishlist_with_items(
        self, client: AsyncClient, auth_headers, test_wishlist
    ):
        resp = await client.get(f"{API}/wishlist", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert len(data) >= 1

    async def test_get_wishlist_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{API}/wishlist")
        assert resp.status_code == 401


class TestAddToWishlist:
    async def test_add_to_wishlist_success(
        self, client: AsyncClient, auth_headers, test_product
    ):
        resp = await client.post(
            f"{API}/wishlist/{test_product.id}", headers=auth_headers
        )
        assert resp.status_code == 201

    async def test_add_duplicate(
        self, client: AsyncClient, auth_headers, test_wishlist, test_product
    ):
        resp = await client.post(
            f"{API}/wishlist/{test_product.id}", headers=auth_headers
        )
        assert resp.status_code == 409

    async def test_add_nonexistent_product(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{API}/wishlist/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestRemoveFromWishlist:
    async def test_remove_success(
        self, client: AsyncClient, auth_headers, test_wishlist, test_product
    ):
        resp = await client.delete(
            f"{API}/wishlist/{test_product.id}", headers=auth_headers
        )
        assert resp.status_code == 200

    async def test_remove_not_in_wishlist(self, client: AsyncClient, auth_headers):
        resp = await client.delete(f"{API}/wishlist/99999", headers=auth_headers)
        assert resp.status_code == 404
