"""
Content router — 內容 API (公開)
GET /content/banners
GET /content/announcements
GET /content/featured-sections
"""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.content import Announcement, Banner, FeaturedSection
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/content", tags=["內容"])


@router.get("/banners", response_model=SuccessResponse)
async def get_banners(
    db: AsyncSession = Depends(get_db),
):
    """取得輪播 Banner"""
    now = datetime.utcnow()
    result = await db.execute(
        select(Banner)
        .where(
            Banner.is_active == True,
            Banner.starts_at <= now,
            (Banner.expires_at == None) | (Banner.expires_at >= now),
        )
        .order_by(Banner.sort_order.asc())
    )
    banners = result.scalars().all()

    data = [
        {
            "id": b.id,
            "title": b.title,
            "subtitle": b.subtitle,
            "image_url": b.image_url,
            "mobile_image_url": b.image_url_mobile,
            "link_url": b.link_url,
        }
        for b in banners
    ]
    return SuccessResponse(data=data)


@router.get("/announcements", response_model=SuccessResponse)
async def get_announcements(
    db: AsyncSession = Depends(get_db),
):
    """取得公告"""
    now = datetime.utcnow()
    result = await db.execute(
        select(Announcement)
        .where(
            Announcement.is_active == True,
            Announcement.starts_at <= now,
            (Announcement.expires_at == None) | (Announcement.expires_at >= now),
        )
        .order_by(Announcement.created_at.desc())
    )
    items = result.scalars().all()

    data = [
        {
            "id": a.id,
            "content": a.content,
            "type": a.type,
            "link_url": a.link_url,
        }
        for a in items
    ]
    return SuccessResponse(data=data)


@router.get("/featured-sections", response_model=SuccessResponse)
async def get_featured_sections(
    db: AsyncSession = Depends(get_db),
):
    """取得首頁精選區塊"""
    result = await db.execute(
        select(FeaturedSection)
        .where(FeaturedSection.is_active == True)
        .order_by(FeaturedSection.sort_order.asc())
    )
    sections = result.scalars().all()

    data = [
        {
            "id": s.id,
            "title": s.title,
            "subtitle": s.subtitle,
            "type": s.type,
            "config": s.config,
        }
        for s in sections
    ]
    return SuccessResponse(data=data)
