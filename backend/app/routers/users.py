"""
Users router — 使用者 API
PUT  /users/profile
PUT  /users/password
GET  /users/addresses
POST /users/addresses
PUT  /users/addresses/:id
DELETE /users/addresses/:id
GET  /users/cards
POST /users/cards
DELETE /users/cards/:id
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, UserAddress, UserCard
from app.schemas.user import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
    CardCreate,
    CardResponse,
    ChangePasswordRequest,
    UserProfileUpdate,
    UserResponse,
)
from app.schemas.common import SuccessResponse
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["使用者"])


# ===== Profile =====

@router.put("/profile", response_model=SuccessResponse)
async def update_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新個人資料"""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)

    return SuccessResponse(
        data=UserResponse.model_validate(current_user).model_dump(),
        message="個人資料更新成功",
    )


@router.put("/password", response_model=SuccessResponse)
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """修改密碼"""
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="目前密碼錯誤",
        )

    current_user.password_hash = hash_password(data.new_password)

    return SuccessResponse(message="密碼修改成功")


# ===== Addresses =====

@router.get("/addresses", response_model=SuccessResponse)
async def list_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得地址清單"""
    result = await db.execute(
        select(UserAddress)
        .where(UserAddress.user_id == current_user.id)
        .order_by(UserAddress.is_default.desc(), UserAddress.created_at.desc())
    )
    addresses = result.scalars().all()

    return SuccessResponse(
        data=[AddressResponse.model_validate(a).model_dump() for a in addresses],
    )


@router.post("/addresses", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_address(
    data: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """新增地址"""
    # If setting as default, unset existing defaults
    if data.is_default:
        result = await db.execute(
            select(UserAddress).where(
                UserAddress.user_id == current_user.id,
                UserAddress.is_default == True,
            )
        )
        for addr in result.scalars().all():
            addr.is_default = False

    address = UserAddress(
        user_id=current_user.id,
        **data.model_dump(),
    )
    db.add(address)
    await db.flush()

    return SuccessResponse(
        data=AddressResponse.model_validate(address).model_dump(),
        message="地址新增成功",
    )


@router.put("/addresses/{address_id}", response_model=SuccessResponse)
async def update_address(
    address_id: int,
    data: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新地址"""
    result = await db.execute(
        select(UserAddress).where(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id,
        )
    )
    address = result.scalar_one_or_none()

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="地址不存在")

    # Handle default flag
    if data.is_default:
        existing = await db.execute(
            select(UserAddress).where(
                UserAddress.user_id == current_user.id,
                UserAddress.is_default == True,
                UserAddress.id != address_id,
            )
        )
        for addr in existing.scalars().all():
            addr.is_default = False

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(address, key, value)

    return SuccessResponse(
        data=AddressResponse.model_validate(address).model_dump(),
        message="地址更新成功",
    )


@router.delete("/addresses/{address_id}", response_model=SuccessResponse)
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """刪除地址"""
    result = await db.execute(
        select(UserAddress).where(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id,
        )
    )
    address = result.scalar_one_or_none()

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="地址不存在")

    await db.delete(address)

    return SuccessResponse(message="地址已刪除")


# ===== Cards =====

@router.get("/cards", response_model=SuccessResponse)
async def list_cards(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得儲存的信用卡"""
    result = await db.execute(
        select(UserCard)
        .where(UserCard.user_id == current_user.id)
        .order_by(UserCard.is_default.desc(), UserCard.created_at.desc())
    )
    cards = result.scalars().all()

    return SuccessResponse(
        data=[CardResponse.model_validate(c).model_dump() for c in cards],
    )


@router.post("/cards", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def add_card(
    data: CardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """新增信用卡"""
    if data.is_default:
        result = await db.execute(
            select(UserCard).where(
                UserCard.user_id == current_user.id,
                UserCard.is_default == True,
            )
        )
        for card in result.scalars().all():
            card.is_default = False

    card = UserCard(
        user_id=current_user.id,
        **data.model_dump(),
    )
    db.add(card)
    await db.flush()

    return SuccessResponse(
        data=CardResponse.model_validate(card).model_dump(),
        message="信用卡新增成功",
    )


@router.delete("/cards/{card_id}", response_model=SuccessResponse)
async def delete_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """刪除信用卡"""
    result = await db.execute(
        select(UserCard).where(
            UserCard.id == card_id,
            UserCard.user_id == current_user.id,
        )
    )
    card = result.scalar_one_or_none()

    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="信用卡不存在")

    await db.delete(card)

    return SuccessResponse(message="信用卡已刪除")
