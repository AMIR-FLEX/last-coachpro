"""
Common Schemas
==============
اسکیماهای مشترک
"""

from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from datetime import datetime

T = TypeVar('T')


class MessageResponse(BaseModel):
    """پاسخ پیام ساده"""
    message: str
    success: bool = True


class PaginatedResponse(BaseModel, Generic[T]):
    """پاسخ صفحه‌بندی شده"""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class TimestampMixin(BaseModel):
    """میکسین برای فیلدهای زمانی"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
