"""
Tests for Auth API endpoints:
  POST /api/v1/auth/register
  POST /api/v1/auth/login
  POST /api/v1/auth/refresh
  POST /api/v1/auth/logout
  POST /api/v1/auth/forgot-password
  POST /api/v1/auth/reset-password
  GET  /api/v1/auth/me
"""

import pytest
from httpx import AsyncClient

API = "/api/v1"


# ── Register ─────────────────────────────────────────────────
class TestRegister:
    async def test_register_success(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/register", json={
            "email": "newuser@example.com",
            "password": "NewPass@123",
            "confirm_password": "NewPass@123",
            "first_name": "New",
            "last_name": "User",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        resp = await client.post(f"{API}/auth/register", json={
            "email": "testuser@example.com",
            "password": "NewPass@123",
            "confirm_password": "NewPass@123",
            "first_name": "Dup",
            "last_name": "User",
        })
        assert resp.status_code == 409

    async def test_register_password_mismatch(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/register", json={
            "email": "mismatch@example.com",
            "password": "NewPass@123",
            "confirm_password": "DifferentPass@123",
            "first_name": "Mis",
            "last_name": "Match",
        })
        assert resp.status_code == 422

    async def test_register_weak_password(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/register", json={
            "email": "weak@example.com",
            "password": "weakpass",
            "confirm_password": "weakpass",
            "first_name": "Weak",
            "last_name": "Pass",
        })
        assert resp.status_code == 422

    async def test_register_invalid_email(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/register", json={
            "email": "not-an-email",
            "password": "NewPass@123",
            "confirm_password": "NewPass@123",
            "first_name": "Bad",
            "last_name": "Email",
        })
        assert resp.status_code == 422

    async def test_register_missing_fields(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/register", json={
            "email": "partial@example.com",
        })
        assert resp.status_code == 422


# ── Login ────────────────────────────────────────────────────
class TestLogin:
    async def test_login_success(self, client: AsyncClient, test_user):
        resp = await client.post(f"{API}/auth/login", json={
            "email": "testuser@example.com",
            "password": "Test@12345",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "access_token" in data["data"]

    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        resp = await client.post(f"{API}/auth/login", json={
            "email": "testuser@example.com",
            "password": "WrongPass@123",
        })
        assert resp.status_code == 401

    async def test_login_nonexistent_email(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/login", json={
            "email": "noone@example.com",
            "password": "AnyPass@123",
        })
        assert resp.status_code == 401

    async def test_login_inactive_user(self, client: AsyncClient, inactive_user):
        resp = await client.post(f"{API}/auth/login", json={
            "email": "inactive@example.com",
            "password": "Test@12345",
        })
        assert resp.status_code == 403


# ── Token Refresh ────────────────────────────────────────────
class TestTokenRefresh:
    async def test_refresh_token_success(self, client: AsyncClient, test_user):
        # Login first
        login_resp = await client.post(f"{API}/auth/login", json={
            "email": "testuser@example.com",
            "password": "Test@12345",
        })
        refresh_token = login_resp.json()["data"]["refresh_token"]

        # Refresh
        resp = await client.post(f"{API}/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data["data"]

    async def test_refresh_token_invalid(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/refresh", json={
            "refresh_token": "invalid-token",
        })
        assert resp.status_code == 401


# ── Logout ───────────────────────────────────────────────────
class TestLogout:
    async def test_logout_success(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{API}/auth/logout", headers=auth_headers)
        assert resp.status_code == 200

    async def test_logout_unauthenticated(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/logout")
        assert resp.status_code == 401


# ── Forgot / Reset Password ─────────────────────────────────
class TestPasswordReset:
    async def test_forgot_password_existing_email(self, client: AsyncClient, test_user):
        resp = await client.post(f"{API}/auth/forgot-password", json={
            "email": "testuser@example.com",
        })
        assert resp.status_code == 200

    async def test_forgot_password_unknown_email(self, client: AsyncClient):
        """Should still return 200 to prevent email enumeration."""
        resp = await client.post(f"{API}/auth/forgot-password", json={
            "email": "unknown@example.com",
        })
        assert resp.status_code == 200

    async def test_reset_password_invalid_token(self, client: AsyncClient):
        resp = await client.post(f"{API}/auth/reset-password", json={
            "token": "bad-token",
            "password": "NewPass@123",
            "confirm_password": "NewPass@123",
        })
        assert resp.status_code == 400


# ── Get Current User ─────────────────────────────────────────
class TestGetMe:
    async def test_get_me_authenticated(self, client: AsyncClient, auth_headers, test_user):
        resp = await client.get(f"{API}/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["email"] == "testuser@example.com"
        assert data["first_name"] == "Test"

    async def test_get_me_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{API}/auth/me")
        assert resp.status_code == 401
