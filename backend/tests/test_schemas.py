"""
Tests for Pydantic schema validation
"""

import pytest
from pydantic import ValidationError

from app.schemas.user import (
    AddressCreate,
    CardCreate,
    ChangePasswordRequest,
    LoginRequest,
    RegisterRequest,
    UserProfileUpdate,
)
from app.schemas.product import ProductCreate, ReviewCreate
from app.schemas.order import CartItemAdd, CartItemUpdate
from app.schemas.common import PaginationParams, SortParams


# ── Auth Schemas ─────────────────────────────────────────────
class TestRegisterSchema:
    def test_valid_register(self):
        data = RegisterRequest(
            email="valid@test.com",
            password="StrongPass@1",
            confirm_password="StrongPass@1",
            first_name="Test",
            last_name="User",
        )
        assert data.email == "valid@test.com"

    def test_password_mismatch(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="x@test.com",
                password="StrongPass@1",
                confirm_password="DifferentPass@1",
                first_name="Test",
                last_name="User",
            )

    def test_password_no_uppercase(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="x@test.com",
                password="nouppercas1",
                confirm_password="nouppercas1",
                first_name="Test",
                last_name="User",
            )

    def test_password_no_digit(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="x@test.com",
                password="NoDigitHere!",
                confirm_password="NoDigitHere!",
                first_name="Test",
                last_name="User",
            )

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="x@test.com",
                password="Ab1!",
                confirm_password="Ab1!",
                first_name="Test",
                last_name="User",
            )

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            RegisterRequest(
                email="not-email",
                password="StrongPass@1",
                confirm_password="StrongPass@1",
                first_name="Test",
                last_name="User",
            )


class TestLoginSchema:
    def test_valid_login(self):
        data = LoginRequest(email="user@test.com", password="Password@1")
        assert data.email == "user@test.com"

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            LoginRequest(email="user@test.com", password="short")


# ── Review Schema ────────────────────────────────────────────
class TestReviewSchema:
    def test_valid_review(self):
        r = ReviewCreate(rating=5, title="Great!", content="Love it")
        assert r.rating == 5

    def test_rating_too_high(self):
        with pytest.raises(ValidationError):
            ReviewCreate(rating=10)

    def test_rating_too_low(self):
        with pytest.raises(ValidationError):
            ReviewCreate(rating=0)


# ── Cart Schemas ─────────────────────────────────────────────
class TestCartSchemas:
    def test_valid_cart_item_add(self):
        item = CartItemAdd(product_id=1, quantity=3)
        assert item.quantity == 3

    def test_cart_item_add_invalid_quantity(self):
        with pytest.raises(ValidationError):
            CartItemAdd(product_id=1, quantity=0)

    def test_cart_item_update(self):
        update = CartItemUpdate(quantity=5)
        assert update.quantity == 5


# ── Product Schema ───────────────────────────────────────────
class TestProductSchema:
    def test_valid_product_create(self):
        p = ProductCreate(name="Test Item", price=100.0)
        assert p.name == "Test Item"

    def test_product_price_must_be_positive(self):
        with pytest.raises(ValidationError):
            ProductCreate(name="Bad Price", price=-10)

    def test_product_stock_non_negative(self):
        with pytest.raises(ValidationError):
            ProductCreate(name="Bad Stock", price=10, stock=-1)


# ── Address Schema ───────────────────────────────────────────
class TestAddressSchema:
    def test_valid_address(self):
        a = AddressCreate(
            recipient_name="John",
            phone="0912345678",
            city="台北市",
            district="信義區",
            address="信義路一段1號",
        )
        assert a.city == "台北市"


# ── Card Schema ──────────────────────────────────────────────
class TestCardSchema:
    def test_valid_card(self):
        c = CardCreate(
            card_token="tok_123",
            last_four="4242",
            card_type="visa",
            expiry_month=12,
            expiry_year=2028,
        )
        assert c.last_four == "4242"

    def test_invalid_expiry_month(self):
        with pytest.raises(ValidationError):
            CardCreate(
                card_token="tok_123",
                last_four="4242",
                card_type="visa",
                expiry_month=13,
                expiry_year=2028,
            )


# ── Pagination Schema ───────────────────────────────────────
class TestPaginationSchema:
    def test_defaults(self):
        p = PaginationParams()
        assert p.page == 1
        assert p.per_page == 20
        assert p.offset == 0

    def test_offset_calculation(self):
        p = PaginationParams(page=3, per_page=10)
        assert p.offset == 20

    def test_invalid_page(self):
        with pytest.raises(ValidationError):
            PaginationParams(page=0)

    def test_sort_params(self):
        s = SortParams(sort_by="price", sort_order="asc")
        assert s.sort_order == "asc"

    def test_invalid_sort_order(self):
        with pytest.raises(ValidationError):
            SortParams(sort_order="random")
