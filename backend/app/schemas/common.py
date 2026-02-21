"""
Common schemas — shared response format, pagination, etc.
"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = 1
    per_page: int = 20
    total: int = 0
    total_pages: int = 0


class SuccessResponse(BaseModel):
    """標準成功回應"""
    success: bool = True
    data: Any = None
    message: str = "操作成功"
    meta: Optional[PaginationMeta] = None


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None


class ErrorResponse(BaseModel):
    """標準錯誤回應"""
    success: bool = False
    error: ErrorBody


class PaginationParams(BaseModel):
    """分頁參數"""
    page: int = Field(default=1, ge=1, description="頁碼")
    per_page: int = Field(default=20, ge=1, le=50, description="每頁筆數")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class SortParams(BaseModel):
    """排序參數"""
    sort_by: str = "created_at"
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class IDResponse(BaseModel):
    """回傳 ID 的簡單回應"""
    id: int
