"""
Popular Food Shop — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import close_db, init_db
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

# ── Import Routers ──────────────────────
from app.routers import auth, brands, cart, categories, content, orders, payments, points, products, users, wishlist
from app.routers.admin import content as admin_content
from app.routers.admin import dashboard as admin_dashboard
from app.routers.admin import orders as admin_orders
from app.routers.admin import products as admin_products
from app.routers.admin import promotions as admin_promotions
from app.routers.admin import reports as admin_reports
from app.routers.admin import settings as admin_settings
from app.routers.admin import users as admin_users

settings = get_settings()


# ── Lifespan ────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup / shutdown events."""
    await init_db()
    yield
    await close_db()


# ── Create App ──────────────────────────
app = FastAPI(
    title="Popular Food Shop API",
    description="美食電商平台 API — 類 ifchic 風格食品電商",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


# ── Middleware (order matters: last added = first executed) ──
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


# ── Exception Handlers ──────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"success": False, "error": {"message": "找不到資源", "code": "NOT_FOUND"}})


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(status_code=500, content={"success": False, "error": {"message": "伺服器內部錯誤", "code": "INTERNAL_ERROR"}})


# ── Public API Routes (/api/v1) ──────────
API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(products.router, prefix=API_PREFIX)
app.include_router(categories.router, prefix=API_PREFIX)
app.include_router(brands.router, prefix=API_PREFIX)
app.include_router(cart.router, prefix=API_PREFIX)
app.include_router(orders.router, prefix=API_PREFIX)
app.include_router(payments.router, prefix=API_PREFIX)
app.include_router(wishlist.router, prefix=API_PREFIX)
app.include_router(points.router, prefix=API_PREFIX)
app.include_router(content.router, prefix=API_PREFIX)

# ── Admin API Routes (/api/v1/admin/*) ───
app.include_router(admin_dashboard.router, prefix=API_PREFIX)
app.include_router(admin_products.router, prefix=API_PREFIX)
app.include_router(admin_orders.router, prefix=API_PREFIX)
app.include_router(admin_users.router, prefix=API_PREFIX)
app.include_router(admin_promotions.router, prefix=API_PREFIX)
app.include_router(admin_content.router, prefix=API_PREFIX)
app.include_router(admin_reports.router, prefix=API_PREFIX)
app.include_router(admin_settings.router, prefix=API_PREFIX)


# ── Health Check ─────────────────────────
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "popular-food-shop-api"}


@app.get("/")
async def root():
    return {
        "message": "Popular Food Shop API",
        "version": "1.0.0",
        "docs": "/api/docs",
    }
