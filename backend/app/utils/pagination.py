"""
Pagination utility
"""

import math
from typing import Any, List, Optional, Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.common import PaginationMeta


async def paginate(
    db: AsyncSession,
    query: Select,
    page: int = 1,
    per_page: int = 20,
) -> tuple[Sequence[Any], PaginationMeta]:
    """
    執行分頁查詢

    Returns:
        (items, meta)
    """
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Calculate pagination
    total_pages = math.ceil(total / per_page) if per_page > 0 else 0
    offset = (page - 1) * per_page

    # Fetch items
    paginated_query = query.offset(offset).limit(per_page)
    result = await db.execute(paginated_query)
    items = result.scalars().all()

    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
    )

    return items, meta
