"""
Tests for Points / Credits API endpoints:
  GET /api/v1/points
  GET /api/v1/points/history
  GET /api/v1/credits
  GET /api/v1/credits/history
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


class TestPoints:
    async def test_get_points_balance(self, client: AsyncClient, auth_headers, test_user):
        resp = await client.get(f"{API}/points", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "points" in data
        assert data["points"] == test_user.points

    async def test_get_points_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{API}/points")
        assert resp.status_code == 401

    async def test_get_points_history(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/points/history", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)

    async def test_get_points_history_pagination(self, client: AsyncClient, auth_headers):
        resp = await client.get(
            f"{API}/points/history",
            headers=auth_headers,
            params={"page": 1, "per_page": 5},
        )
        assert resp.status_code == 200


class TestCredits:
    async def test_get_credits_balance(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/credits", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "credits" in data

    async def test_get_credits_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{API}/credits")
        assert resp.status_code == 401

    async def test_get_credits_history(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/credits/history", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)
