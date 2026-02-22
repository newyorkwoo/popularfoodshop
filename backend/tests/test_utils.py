"""
Tests for utility functions: security, helpers, pagination
"""

from datetime import timedelta

import pytest

from app.utils.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    verify_password_reset_token,
)
from app.utils.helpers import (
    format_price,
    generate_order_number,
    generate_random_code,
    generate_slug,
)


# ── Password Hashing ────────────────────────────────────────
class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        result = hash_password("MySecurePass123")
        assert isinstance(result, str)
        assert result != "MySecurePass123"

    def test_verify_correct_password(self):
        hashed = hash_password("TestPassword@1")
        assert verify_password("TestPassword@1", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("TestPassword@1")
        assert verify_password("WrongPassword@1", hashed) is False

    def test_different_hashes_for_same_password(self):
        h1 = hash_password("SamePass1!")
        h2 = hash_password("SamePass1!")
        assert h1 != h2  # bcrypt uses random salt


# ── JWT Tokens ───────────────────────────────────────────────
class TestJWTTokens:
    def test_create_access_token_returns_string(self):
        token = create_access_token(user_id=1, role="customer")
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_refresh_token_returns_string(self):
        token = create_refresh_token(user_id=1)
        assert isinstance(token, str)
        assert len(token) > 20

    def test_access_token_custom_expiry(self):
        token = create_access_token(
            user_id=99, role="admin", expires_delta=timedelta(minutes=5)
        )
        assert isinstance(token, str)

    def test_decode_invalid_token(self):
        result = decode_token("invalid.token.here")
        assert result is None

    def test_decode_empty_token(self):
        result = decode_token("")
        assert result is None

    def test_password_reset_token_roundtrip(self):
        email = "test@example.com"
        token = create_password_reset_token(email)
        recovered_email = verify_password_reset_token(token)
        assert recovered_email == email

    def test_password_reset_token_invalid(self):
        result = verify_password_reset_token("bad-token")
        assert result is None

    def test_access_token_not_valid_as_password_reset(self):
        token = create_access_token(user_id=1, role="customer")
        result = verify_password_reset_token(token)
        assert result is None

    def test_different_tokens_for_different_users(self):
        t1 = create_access_token(user_id=1, role="customer")
        t2 = create_access_token(user_id=2, role="customer")
        assert t1 != t2


# ── Helpers ──────────────────────────────────────────────────
class TestHelpers:
    def test_generate_slug(self):
        assert generate_slug("Hello World") == "hello-world"
        assert generate_slug("日本零食 Premium") is not None
        assert " " not in generate_slug("spaces in here")

    def test_generate_order_number_format(self):
        order_num = generate_order_number()
        assert order_num.startswith("PFS")
        assert len(order_num) == 17  # PFS + 8 date + 6 random

    def test_generate_order_number_uniqueness(self):
        numbers = {generate_order_number() for _ in range(50)}
        assert len(numbers) == 50  # All unique

    def test_generate_random_code_default_length(self):
        code = generate_random_code()
        assert len(code) == 8
        assert code.isalnum()

    def test_generate_random_code_custom_length(self):
        code = generate_random_code(length=12)
        assert len(code) == 12

    def test_format_price_twd(self):
        assert format_price(1500) == "NT$1,500"
        assert format_price(99) == "NT$99"

    def test_format_price_usd(self):
        assert format_price(29.99, "USD") == "$29.99"
