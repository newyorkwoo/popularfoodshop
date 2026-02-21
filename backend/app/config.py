"""
Popular Food Shop — Application Configuration
使用 pydantic-settings 管理環境變數
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """應用程式設定"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ===== Application =====
    APP_NAME: str = "Popular Food Shop"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development | staging | production

    # ===== Server =====
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    API_PREFIX: str = "/api/v1"

    # ===== Database =====
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/popularfoodshop"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_TIMEOUT: int = 30
    DB_ECHO: bool = False

    # ===== Redis =====
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PREFIX: str = "pfs:"

    # ===== JWT =====
    JWT_SECRET_KEY: str = "change-me-to-a-secure-random-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== Security =====
    SECRET_KEY: str = "change-me-to-another-secure-random-key"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    ALLOWED_HOSTS: List[str] = ["*"]

    # ===== Rate Limiting =====
    RATE_LIMIT_LOGIN: str = "5/minute"
    RATE_LIMIT_REGISTER: str = "3/hour"
    RATE_LIMIT_API: str = "100/minute"
    RATE_LIMIT_SEARCH: str = "30/minute"

    # ===== File Upload =====
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    UPLOAD_DIR: str = "uploads"

    # ===== S3 / Cloudflare R2 =====
    S3_ENDPOINT_URL: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET_NAME: str = "popularfoodshop-assets"
    S3_REGION: str = "auto"
    S3_PUBLIC_URL: str = ""  # CDN URL for public access

    # ===== SMTP / Email =====
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "Popular Food Shop"
    SMTP_FROM_EMAIL: str = "noreply@popularfoodshop.com"
    SMTP_USE_TLS: bool = True

    # ===== Payment (ECPay 綠界) =====
    ECPAY_MERCHANT_ID: str = ""
    ECPAY_HASH_KEY: str = ""
    ECPAY_HASH_IV: str = ""
    ECPAY_API_URL: str = "https://payment-stage.ecpay.com.tw"

    # ===== Business Rules =====
    FREE_SHIPPING_THRESHOLD: int = 1500  # 滿 1500 免運
    DEFAULT_SHIPPING_FEE: int = 100
    POINTS_RATE: float = 0.01  # 消費 1 元累積 0.01 點
    POINTS_REDEEM_RATE: float = 1.0  # 1 點 = 1 元
    POINTS_EXPIRY_DAYS: int = 365
    REGISTER_BONUS_POINTS: int = 100

    # ===== Pagination =====
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 50

    @property
    def async_database_url(self) -> str:
        """確保使用 asyncpg 驅動"""
        if "asyncpg" not in self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return self.DATABASE_URL


@lru_cache()
def get_settings() -> Settings:
    """取得快取的設定實例"""
    return Settings()
