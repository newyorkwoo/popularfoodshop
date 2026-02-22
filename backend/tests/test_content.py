"""
Tests for Content API endpoints:
  GET /api/v1/content/banners
  GET /api/v1/content/announcements
  GET /api/v1/content/featured-sections

And health / root endpoints:
  GET /api/health
  GET /
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


class TestHealthCheck:
    async def test_health(self, client: AsyncClient):
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    async def test_root(self, client: AsyncClient):
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "Popular Food Shop" in data["message"]
        assert data["version"] == "1.0.0"


class TestContentBanners:
    async def test_get_banners_empty(self, client: AsyncClient):
        resp = await client.get(f"{API}/content/banners")
        assert resp.status_code == 200
        assert isinstance(resp.json()["data"], list)


class TestContentAnnouncements:
    async def test_get_announcements_empty(self, client: AsyncClient):
        resp = await client.get(f"{API}/content/announcements")
        assert resp.status_code == 200
        assert isinstance(resp.json()["data"], list)


class TestContentFeaturedSections:
    async def test_get_featured_sections_empty(self, client: AsyncClient):
        resp = await client.get(f"{API}/content/featured-sections")
        assert resp.status_code == 200
        assert isinstance(resp.json()["data"], list)
