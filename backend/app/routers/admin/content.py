"""
Admin Content router — 內容管理 API
CRUD /admin/content/banners
CRUD /admin/content/announcements
CRUD /admin/content/featured-sections
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_permission
from app.models.content import Announcement, Banner, FeaturedSection
from app.schemas.common import SuccessResponse
from app.utils.pagination import paginate
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/admin/content", tags=["管理後台 - 內容"])


# ── Schemas ─────────────────────────────
class BannerCreate(BaseModel):
    title: str
    subtitle: Optional[str] = None
    image_url: str
    mobile_image_url: Optional[str] = None
    link_url: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class BannerUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    image_url: Optional[str] = None
    mobile_image_url: Optional[str] = None
    link_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    type: str = "info"
    link_url: Optional[str] = None
    is_active: bool = True
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    link_url: Optional[str] = None
    is_active: Optional[bool] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class FeaturedSectionCreate(BaseModel):
    title: str
    subtitle: Optional[str] = None
    type: str
    config: Optional[dict] = None
    sort_order: int = 0
    is_active: bool = True


class FeaturedSectionUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    type: Optional[str] = None
    config: Optional[dict] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


# ── Banners ─────────────────────────────
@router.get("/banners", response_model=SuccessResponse)
async def list_banners(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    _=Depends(require_permission("content.read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Banner).order_by(Banner.sort_order.asc())
    items, meta = await paginate(db, query, page, per_page)
    data = [
        {
            "id": b.id, "title": b.title, "subtitle": b.subtitle,
            "image_url": b.image_url, "mobile_image_url": b.mobile_image_url,
            "link_url": b.link_url, "sort_order": b.sort_order,
            "is_active": b.is_active,
            "starts_at": b.starts_at.isoformat() if b.starts_at else None,
            "ends_at": b.ends_at.isoformat() if b.ends_at else None,
        }
        for b in items
    ]
    return SuccessResponse(data=data, meta=meta)


@router.post("/banners", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_banner(
    data: BannerCreate,
    _=Depends(require_permission("content.write")),
    db: AsyncSession = Depends(get_db),
):
    banner = Banner(**data.model_dump())
    db.add(banner)
    await db.flush()
    return SuccessResponse(data={"id": banner.id}, message="Banner 已建立")


@router.put("/banners/{banner_id}", response_model=SuccessResponse)
async def update_banner(
    banner_id: int,
    data: BannerUpdate,
    _=Depends(require_permission("content.write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Banner).where(Banner.id == banner_id))
    banner = result.scalar_one_or_none()
    if not banner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner 不存在")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(banner, field, value)
    return SuccessResponse(data={"id": banner.id}, message="Banner 已更新")


@router.delete("/banners/{banner_id}", response_model=SuccessResponse)
async def delete_banner(
    banner_id: int,
    _=Depends(require_permission("content.delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Banner).where(Banner.id == banner_id))
    banner = result.scalar_one_or_none()
    if not banner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner 不存在")
    await db.delete(banner)
    return SuccessResponse(data={"message": "Banner 已刪除"})


# ── Announcements ───────────────────────
@router.get("/announcements", response_model=SuccessResponse)
async def list_announcements(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    _=Depends(require_permission("content.read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Announcement).order_by(Announcement.created_at.desc())
    items, meta = await paginate(db, query, page, per_page)
    data = [
        {
            "id": a.id, "title": a.title, "content": a.content,
            "type": a.type, "link_url": a.link_url,
            "is_active": a.is_active,
            "starts_at": a.starts_at.isoformat() if a.starts_at else None,
            "ends_at": a.ends_at.isoformat() if a.ends_at else None,
        }
        for a in items
    ]
    return SuccessResponse(data=data, meta=meta)


@router.post("/announcements", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    data: AnnouncementCreate,
    _=Depends(require_permission("content.write")),
    db: AsyncSession = Depends(get_db),
):
    ann = Announcement(**data.model_dump())
    db.add(ann)
    await db.flush()
    return SuccessResponse(data={"id": ann.id}, message="公告已建立")


@router.put("/announcements/{ann_id}", response_model=SuccessResponse)
async def update_announcement(
    ann_id: int,
    data: AnnouncementUpdate,
    _=Depends(require_permission("content.write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Announcement).where(Announcement.id == ann_id))
    ann = result.scalar_one_or_none()
    if not ann:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="公告不存在")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ann, field, value)
    return SuccessResponse(data={"id": ann.id}, message="公告已更新")


@router.delete("/announcements/{ann_id}", response_model=SuccessResponse)
async def delete_announcement(
    ann_id: int,
    _=Depends(require_permission("content.delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Announcement).where(Announcement.id == ann_id))
    ann = result.scalar_one_or_none()
    if not ann:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="公告不存在")
    await db.delete(ann)
    return SuccessResponse(data={"message": "公告已刪除"})


# ── Featured Sections ───────────────────
@router.get("/featured-sections", response_model=SuccessResponse)
async def list_featured_sections(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=50),
    _=Depends(require_permission("content.read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(FeaturedSection).order_by(FeaturedSection.sort_order.asc())
    items, meta = await paginate(db, query, page, per_page)
    data = [
        {
            "id": s.id, "title": s.title, "subtitle": s.subtitle,
            "type": s.type, "config": s.config,
            "sort_order": s.sort_order, "is_active": s.is_active,
        }
        for s in items
    ]
    return SuccessResponse(data=data, meta=meta)


@router.post("/featured-sections", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_featured_section(
    data: FeaturedSectionCreate,
    _=Depends(require_permission("content.write")),
    db: AsyncSession = Depends(get_db),
):
    section = FeaturedSection(**data.model_dump())
    db.add(section)
    await db.flush()
    return SuccessResponse(data={"id": section.id}, message="區塊已建立")


@router.put("/featured-sections/{section_id}", response_model=SuccessResponse)
async def update_featured_section(
    section_id: int,
    data: FeaturedSectionUpdate,
    _=Depends(require_permission("content.write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(FeaturedSection).where(FeaturedSection.id == section_id))
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="區塊不存在")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    return SuccessResponse(data={"id": section.id}, message="區塊已更新")


@router.delete("/featured-sections/{section_id}", response_model=SuccessResponse)
async def delete_featured_section(
    section_id: int,
    _=Depends(require_permission("content.delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(FeaturedSection).where(FeaturedSection.id == section_id))
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="區塊不存在")
    await db.delete(section)
    return SuccessResponse(data={"message": "區塊已刪除"})
