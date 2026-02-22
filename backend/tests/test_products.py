"""
Tests for Products API endpoints:
  GET  /api/v1/products
  GET  /api/v1/products/search
  GET  /api/v1/products/trending
  GET  /api/v1/products/:id
  GET  /api/v1/products/:id/reviews
  POST /api/v1/products/:id/reviews
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


# ── List Products ────────────────────────────────────────────
class TestListProducts:
    async def test_list_products_empty(self, client: AsyncClient):
        resp = await client.get(f"{API}/products")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)

    async def test_list_products_with_data(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products")
        assert resp.status_code == 200
        products = resp.json()["data"]
        assert len(products) >= 1
        assert products[0]["name"] == "Test Product"

    async def test_list_products_filter_by_category(
        self, client: AsyncClient, test_product, test_category
    ):
        resp = await client.get(f"{API}/products", params={"category_id": test_category.id})
        assert resp.status_code == 200
        products = resp.json()["data"]
        assert len(products) >= 1

    async def test_list_products_filter_by_brand(
        self, client: AsyncClient, test_product, test_brand
    ):
        resp = await client.get(f"{API}/products", params={"brand_id": test_brand.id})
        assert resp.status_code == 200
        products = resp.json()["data"]
        assert len(products) >= 1

    async def test_list_products_filter_by_price_range(
        self, client: AsyncClient, test_product
    ):
        resp = await client.get(
            f"{API}/products", params={"min_price": 100, "max_price": 600}
        )
        assert resp.status_code == 200
        products = resp.json()["data"]
        assert len(products) >= 1

    async def test_list_products_sort_by_price(self, client: AsyncClient, test_product):
        resp = await client.get(
            f"{API}/products", params={"sort_by": "price", "sort_order": "asc"}
        )
        assert resp.status_code == 200

    async def test_list_products_pagination(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products", params={"page": 1, "per_page": 5})
        assert resp.status_code == 200
        meta = resp.json().get("meta")
        assert meta is not None
        assert meta["page"] == 1
        assert meta["per_page"] == 5


# ── Search Products ──────────────────────────────────────────
class TestSearchProducts:
    async def test_search_by_name(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products/search", params={"q": "Test"})
        assert resp.status_code == 200
        products = resp.json()["data"]
        assert len(products) >= 1

    async def test_search_no_results(self, client: AsyncClient, test_product):
        resp = await client.get(
            f"{API}/products/search", params={"q": "NonExistentXYZ"}
        )
        assert resp.status_code == 200
        assert len(resp.json()["data"]) == 0

    async def test_search_missing_query(self, client: AsyncClient):
        resp = await client.get(f"{API}/products/search")
        assert resp.status_code == 422


# ── Trending Products ────────────────────────────────────────
class TestTrendingProducts:
    async def test_trending(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products/trending")
        assert resp.status_code == 200
        products = resp.json()["data"]
        assert isinstance(products, list)

    async def test_trending_custom_limit(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products/trending", params={"limit": 5})
        assert resp.status_code == 200


# ── Product Detail ───────────────────────────────────────────
class TestProductDetail:
    async def test_get_product_success(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products/{test_product.id}")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["name"] == "Test Product"
        assert data["slug"] == "test-product"
        assert data["price"] == 500.0
        assert data["sale_price"] == 399.0
        assert len(data["images"]) >= 1
        assert len(data["variants"]) >= 1

    async def test_get_product_not_found(self, client: AsyncClient):
        resp = await client.get(f"{API}/products/99999")
        assert resp.status_code == 404

    async def test_view_count_increments(self, client: AsyncClient, test_product):
        initial_views = test_product.view_count
        await client.get(f"{API}/products/{test_product.id}")
        resp = await client.get(f"{API}/products/{test_product.id}")
        data = resp.json()["data"]
        assert data["view_count"] > initial_views


# ── Reviews ──────────────────────────────────────────────────
class TestReviews:
    async def test_list_reviews_empty(self, client: AsyncClient, test_product):
        resp = await client.get(f"{API}/products/{test_product.id}/reviews")
        assert resp.status_code == 200
        assert isinstance(resp.json()["data"], list)

    async def test_create_review(
        self, client: AsyncClient, auth_headers, test_product
    ):
        resp = await client.post(
            f"{API}/products/{test_product.id}/reviews",
            headers=auth_headers,
            json={
                "rating": 5,
                "title": "Great product!",
                "content": "Love it, very tasty.",
            },
        )
        assert resp.status_code == 201
        data = resp.json()["data"]
        assert data["rating"] == 5

    async def test_create_review_unauthenticated(self, client: AsyncClient, test_product):
        resp = await client.post(
            f"{API}/products/{test_product.id}/reviews",
            json={"rating": 4, "title": "OK"},
        )
        assert resp.status_code == 401

    async def test_create_review_invalid_rating(
        self, client: AsyncClient, auth_headers, test_product
    ):
        resp = await client.post(
            f"{API}/products/{test_product.id}/reviews",
            headers=auth_headers,
            json={"rating": 10},
        )
        assert resp.status_code == 422

    async def test_create_review_duplicate(
        self, client: AsyncClient, auth_headers, test_product
    ):
        # Create first review
        await client.post(
            f"{API}/products/{test_product.id}/reviews",
            headers=auth_headers,
            json={"rating": 4, "title": "First"},
        )
        # Try duplicate
        resp = await client.post(
            f"{API}/products/{test_product.id}/reviews",
            headers=auth_headers,
            json={"rating": 3, "title": "Second"},
        )
        assert resp.status_code == 409

    async def test_create_review_product_not_found(
        self, client: AsyncClient, auth_headers
    ):
        resp = await client.post(
            f"{API}/products/99999/reviews",
            headers=auth_headers,
            json={"rating": 5},
        )
        assert resp.status_code == 404
