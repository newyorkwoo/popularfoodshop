"""
Points router — 點數/購物金 API
GET  /points
GET  /points/history
GET  /credits
GET  /credits/history
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.points import PointsTransaction, CreditsTransaction
from app.schemas.common import SuccessResponse
from app.utils.pagination import paginate

router = APIRouter(tags=["點數 / 購物金"])


@router.get("/points", response_model=SuccessResponse)
async def get_points(
    current_user=Depends(get_current_user),
):
    """取得點數餘額"""
    return SuccessResponse(data={
        "points": current_user.points,
    })


@router.get("/points/history", response_model=SuccessResponse)
async def points_history(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得點數歷史紀錄"""
    query = (
        select(PointsTransaction)
        .where(PointsTransaction.user_id == current_user.id)
        .order_by(PointsTransaction.created_at.desc())
    )
    items, meta = await paginate(db, query, page, per_page)

    data = [
        {
            "id": t.id,
            "type": t.type,
            "amount": t.amount,
            "description": t.description,
            "created_at": t.created_at.isoformat(),
        }
        for t in items
    ]

    return SuccessResponse(data=data, meta=meta)


@router.get("/credits", response_model=SuccessResponse)
async def get_credits(
    current_user=Depends(get_current_user),
):
    """取得購物金餘額"""
    return SuccessResponse(data={
        "credits": float(current_user.credits),
    })


@router.get("/credits/history", response_model=SuccessResponse)
async def credits_history(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取得購物金歷史紀錄"""
    query = (
        select(CreditsTransaction)
        .where(CreditsTransaction.user_id == current_user.id)
        .order_by(CreditsTransaction.created_at.desc())
    )
    items, meta = await paginate(db, query, page, per_page)

    data = [
        {
            "id": t.id,
            "type": t.type,
            "amount": float(t.amount),
            "description": t.description,
            "created_at": t.created_at.isoformat(),
        }
        for t in items
    ]

    return SuccessResponse(data=data, meta=meta)
