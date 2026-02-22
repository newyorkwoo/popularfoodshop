"""
Tests for Categories and Brands API endpoints:
  GET /api/v1/categories
  GET /api/v1/categories/:slug
  GET /api/v1/categories/:slug/products
  GET /api/v1/brands
  GET /api/v1/brands/:slug
  GET /api/v1/brands/:slug/products
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


# ── Categories ───────────────────────────────────────────────
class TestCategories:
    async def test_list_categories_empty(self, client: AsyncClient):
        resp = await client.get(f"{API}/categories")
        assert resp.status_code == 200
        assert isinstance(resp.json()["data"], list)

    async def test_list_categories_with_data(
        self, client: AsyncClient, test_category
    ):
        resp = await client.get(f"{API}/categories")
        assert resp.status_code == 200
        categories = resp.json()["data"]
        assert len(categories) >= 1

    async def test_get_category_by_slug(self, client: AsyncClient, test_category):
        resp = await client.get(f"{API}/categories/{test_category.slug}")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["name"] == "Test Category"

    async def test_get_category_not_found(self, client: AsyncClient):
        resp = await client.get(f"{API}/categories/nonexistent-slug")
        assert resp.status_code == 404

    async def test_category_products(
        self, client: AsyncClient, test_category, test_product
    ):
        resp = await client.get(f"{API}/categories/{test_category.slug}/products")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "products" in data
        assert len(data["products"]) >= 1


# ── Brands ───────────────────────────────────────────────────
class TestBrands:
    async def test_list_brands_empty(self, client: AsyncClient):
        resp = await client.get(f"{API}/brands")
        assert resp.status_code == 200
        assert isinstance(resp.json()["data"], list)

    async def test_list_brands_with_data(self, client: AsyncClient, test_brand):
        resp = await client.get(f"{API}/brands")
        assert resp.status_code == 200
        brands = resp.json()["data"]
        assert len(brands) >= 1

    async def test_get_brand_by_slug(self, client: AsyncClient, test_brand):
        resp = await client.get(f"{API}/brands/{test_brand.slug}")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["name"] == "Test Brand"

    async def test_get_brand_not_found(self, client: AsyncClient):
        resp = await client.get(f"{API}/brands/nonexistent-slug")
        assert resp.status_code == 404

    async def test_brand_products(
        self, client: AsyncClient, test_brand, test_product
    ):
        resp = await client.get(f"{API}/brands/{test_brand.slug}/products")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "products" in data
        assert len(data["products"]) >= 1
