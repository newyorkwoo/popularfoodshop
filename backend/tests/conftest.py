"""
Shared test fixtures for Popular Food Shop backend tests.
Uses SQLite in-memory database for fast isolated testing.
"""

import asyncio
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.types import JSON

from app.database import Base, get_db
from app.main import app
from app.models.brand import Brand
from app.models.cart import CartItem
from app.models.category import Category
from app.models.product import Product, ProductImage, ProductReview, ProductVariant
from app.models.user import User, UserAddress
from app.models.wishlist import Wishlist
from app.models.order import Order, OrderItem, OrderStatusLog
from app.models.points import PointsTransaction
from app.utils.security import create_access_token, hash_password

# ── Map PostgreSQL-specific types to SQLite-compatible ones ──
# Replace JSONB with JSON for SQLite compatibility
for table in Base.metadata.tables.values():
    for column in table.columns:
        if isinstance(column.type, JSONB):
            column.type = JSON()

# ── In-memory SQLite async engine for tests ─────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ── Override dependency ──────────────────────────────────────
async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


# ── Event loop ───────────────────────────────────────────────
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ── DB setup / teardown ─────────────────────────────────────
@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Create all tables before each test, drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ── DB Session ───────────────────────────────────────────────
@pytest_asyncio.fixture
async def db():
    async with TestSessionLocal() as session:
        yield session


# ── Async HTTP client ────────────────────────────────────────
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ── Test Users ───────────────────────────────────────────────
@pytest_asyncio.fixture
async def test_user(db: AsyncSession):
    """Create a regular customer user."""
    user = User(
        email="testuser@example.com",
        password_hash=hash_password("Test@12345"),
        first_name="Test",
        last_name="User",
        phone="0912345678",
        role="customer",
        is_active=True,
        is_verified=True,
        points=100,
        credits=0,
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_user(db: AsyncSession):
    """Create an admin user."""
    user = User(
        email="admin@example.com",
        password_hash=hash_password("Admin@12345"),
        first_name="Admin",
        last_name="User",
        role="super_admin",
        is_active=True,
        is_verified=True,
        points=0,
        credits=0,
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def inactive_user(db: AsyncSession):
    """Create an inactive user."""
    user = User(
        email="inactive@example.com",
        password_hash=hash_password("Test@12345"),
        first_name="Inactive",
        last_name="User",
        role="customer",
        is_active=False,
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user


# ── Auth Tokens ──────────────────────────────────────────────
@pytest_asyncio.fixture
async def user_token(test_user: User):
    """JWT access token for test_user."""
    return create_access_token(test_user.id, test_user.role)


@pytest_asyncio.fixture
async def admin_token(admin_user: User):
    """JWT access token for admin_user."""
    return create_access_token(admin_user.id, admin_user.role)


@pytest_asyncio.fixture
async def auth_headers(user_token: str):
    """Authorization headers for test_user."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest_asyncio.fixture
async def admin_headers(admin_token: str):
    """Authorization headers for admin_user."""
    return {"Authorization": f"Bearer {admin_token}"}


# ── Seed Data ────────────────────────────────────────────────
@pytest_asyncio.fixture
async def test_brand(db: AsyncSession):
    brand = Brand(
        name="Test Brand",
        slug="test-brand",
        description="A brand for testing",
        country="Taiwan",
        is_active=True,
    )
    db.add(brand)
    await db.flush()
    await db.commit()
    await db.refresh(brand)
    return brand


@pytest_asyncio.fixture
async def test_category(db: AsyncSession):
    category = Category(
        name="Test Category",
        slug="test-category",
        description="A category for testing",
        is_active=True,
    )
    db.add(category)
    await db.flush()
    await db.commit()
    await db.refresh(category)
    return category


@pytest_asyncio.fixture
async def test_product(db: AsyncSession, test_brand: Brand, test_category: Category):
    product = Product(
        name="Test Product",
        slug="test-product",
        description="A product for testing",
        short_description="Short desc",
        price=500.00,
        sale_price=399.00,
        sku="TEST-001",
        stock=50,
        brand_id=test_brand.id,
        category_id=test_category.id,
        is_active=True,
        is_new=True,
        is_featured=True,
        avg_rating=4.5,
        review_count=10,
        sold_count=100,
        view_count=500,
        origin="台灣",
        tags=["有機", "無糖"],
    )
    db.add(product)
    await db.flush()

    # Add image
    image = ProductImage(
        product_id=product.id,
        url="https://example.com/test-product.jpg",
        alt_text="Test product image",
        sort_order=0,
    )
    db.add(image)

    # Add variant
    variant = ProductVariant(
        product_id=product.id,
        name="500g",
        sku="TEST-001-500G",
        price_adjustment=0,
        stock=30,
        is_active=True,
    )
    db.add(variant)

    await db.commit()
    await db.refresh(product)
    return product


@pytest_asyncio.fixture
async def second_product(db: AsyncSession, test_brand: Brand, test_category: Category):
    product = Product(
        name="Second Product",
        slug="second-product",
        price=800.00,
        stock=20,
        brand_id=test_brand.id,
        category_id=test_category.id,
        is_active=True,
    )
    db.add(product)
    await db.flush()
    await db.commit()
    await db.refresh(product)
    return product


@pytest_asyncio.fixture
async def test_address(db: AsyncSession, test_user: User):
    addr = UserAddress(
        user_id=test_user.id,
        label="Home",
        recipient_name="Test User",
        phone="0912345678",
        zip_code="100",
        city="台北市",
        district="中正區",
        address="測試路123號",
        is_default=True,
    )
    db.add(addr)
    await db.flush()
    await db.commit()
    await db.refresh(addr)
    return addr


@pytest_asyncio.fixture
async def test_cart_item(db: AsyncSession, test_user: User, test_product: Product):
    item = CartItem(
        user_id=test_user.id,
        product_id=test_product.id,
        quantity=2,
    )
    db.add(item)
    await db.flush()
    await db.commit()
    await db.refresh(item)
    return item


@pytest_asyncio.fixture
async def test_wishlist(db: AsyncSession, test_user: User, test_product: Product):
    w = Wishlist(
        user_id=test_user.id,
        product_id=test_product.id,
    )
    db.add(w)
    await db.flush()
    await db.commit()
    await db.refresh(w)
    return w
