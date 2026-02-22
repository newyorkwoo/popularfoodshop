"""
Tests for Users API endpoints:
  PUT    /api/v1/users/profile
  PUT    /api/v1/users/password
  GET    /api/v1/users/addresses
  POST   /api/v1/users/addresses
  PUT    /api/v1/users/addresses/:id
  DELETE /api/v1/users/addresses/:id
  GET    /api/v1/users/cards
  POST   /api/v1/users/cards
  DELETE /api/v1/users/cards/:id
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


# ── Profile ──────────────────────────────────────────────────
class TestProfile:
    async def test_update_profile(self, client: AsyncClient, auth_headers):
        resp = await client.put(f"{API}/users/profile", headers=auth_headers, json={
            "first_name": "Updated",
            "phone": "0988777666",
        })
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["first_name"] == "Updated"

    async def test_update_profile_unauthenticated(self, client: AsyncClient):
        resp = await client.put(f"{API}/users/profile", json={"first_name": "X"})
        assert resp.status_code == 401


# ── Password Change ──────────────────────────────────────────
class TestPasswordChange:
    async def test_change_password_success(self, client: AsyncClient, auth_headers):
        resp = await client.put(f"{API}/users/password", headers=auth_headers, json={
            "current_password": "Test@12345",
            "new_password": "NewPass@99999",
            "confirm_password": "NewPass@99999",
        })
        assert resp.status_code == 200

    async def test_change_password_wrong_current(self, client: AsyncClient, auth_headers):
        resp = await client.put(f"{API}/users/password", headers=auth_headers, json={
            "current_password": "WrongCurrent@1",
            "new_password": "NewPass@99999",
            "confirm_password": "NewPass@99999",
        })
        assert resp.status_code == 400


# ── Addresses ────────────────────────────────────────────────
class TestAddresses:
    async def test_list_addresses_empty(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/users/addresses", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["data"] == [] or isinstance(resp.json()["data"], list)

    async def test_create_address(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{API}/users/addresses", headers=auth_headers, json={
            "label": "公司",
            "recipient_name": "Test User",
            "phone": "0911222333",
            "zip_code": "106",
            "city": "台北市",
            "district": "大安區",
            "address": "信義路100號",
            "is_default": True,
        })
        assert resp.status_code == 201
        data = resp.json()["data"]
        assert data["label"] == "公司"
        assert data["is_default"] is True

    async def test_update_address(self, client: AsyncClient, auth_headers, test_address):
        resp = await client.put(
            f"{API}/users/addresses/{test_address.id}",
            headers=auth_headers,
            json={
                "label": "Updated",
                "recipient_name": "New Name",
                "phone": "0933444555",
                "city": "高雄市",
                "district": "前鎮區",
                "address": "中山路50號",
            },
        )
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["label"] == "Updated"
        assert data["city"] == "高雄市"

    async def test_update_address_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.put(
            f"{API}/users/addresses/99999",
            headers=auth_headers,
            json={
                "label": "X",
                "recipient_name": "X",
                "phone": "000",
                "city": "X",
                "district": "X",
                "address": "X",
            },
        )
        assert resp.status_code == 404

    async def test_delete_address(self, client: AsyncClient, auth_headers, test_address):
        resp = await client.delete(
            f"{API}/users/addresses/{test_address.id}",
            headers=auth_headers,
        )
        assert resp.status_code == 200

    async def test_delete_address_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.delete(f"{API}/users/addresses/99999", headers=auth_headers)
        assert resp.status_code == 404


# ── Cards ────────────────────────────────────────────────────
class TestCards:
    async def test_list_cards_empty(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{API}/users/cards", headers=auth_headers)
        assert resp.status_code == 200

    async def test_add_card(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{API}/users/cards", headers=auth_headers, json={
            "card_token": "tok_test_12345",
            "last_four": "4242",
            "card_type": "visa",
            "expiry_month": 12,
            "expiry_year": 2028,
            "is_default": True,
        })
        assert resp.status_code == 201
        data = resp.json()["data"]
        assert data["last_four"] == "4242"
        assert data["card_type"] == "visa"

    async def test_delete_card_not_found(self, client: AsyncClient, auth_headers):
        resp = await client.delete(f"{API}/users/cards/99999", headers=auth_headers)
        assert resp.status_code == 404
