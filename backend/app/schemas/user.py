"""
User & Auth schemas
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ===== Auth Schemas =====

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    remember_me: bool = False


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    agree_terms: bool = True

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("密碼不一致")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("密碼至少需包含一個大寫字母")
        if not any(c.islower() for c in v):
            raise ValueError("密碼至少需包含一個小寫字母")
        if not any(c.isdigit() for c in v):
            raise ValueError("密碼至少需包含一個數字")
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("密碼不一致")
        return v


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("密碼不一致")
        return v


# ===== User Schemas =====

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    points: int
    credits: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    avatar_url: Optional[str] = None


class UserAdminUpdate(BaseModel):
    """管理員更新使用者"""
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    points: Optional[int] = None
    credits: Optional[int] = None


class UserListResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    order_count: int = 0
    total_spent: float = 0

    class Config:
        from_attributes = True


# ===== Address Schemas =====

class AddressBase(BaseModel):
    label: Optional[str] = Field(default=None, max_length=50)
    recipient_name: str = Field(max_length=100)
    phone: str = Field(max_length=20)
    zip_code: Optional[str] = Field(default=None, max_length=10)
    city: str = Field(max_length=50)
    district: str = Field(max_length=50)
    address: str = Field(max_length=255)
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Card Schemas =====

class CardCreate(BaseModel):
    card_token: str
    last_four: str = Field(min_length=4, max_length=4)
    card_type: str
    expiry_month: int = Field(ge=1, le=12)
    expiry_year: int
    is_default: bool = False


class CardResponse(BaseModel):
    id: int
    last_four: str
    card_type: str
    expiry_month: int
    expiry_year: int
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True
