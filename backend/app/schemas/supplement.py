"""
Supplement Schemas
==================
اسکیماهای مکمل
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ===== Category Schemas =====

class SupplementCategoryBase(BaseModel):
    """فیلدهای پایه دسته‌بندی مکمل"""
    name: str = Field(..., max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    icon: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    sort_order: int = 0


class SupplementCategoryCreate(SupplementCategoryBase):
    """ایجاد دسته‌بندی"""
    pass


class SupplementCategoryResponse(SupplementCategoryBase):
    """پاسخ دسته‌بندی"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Supplement Schemas =====

class SupplementBase(BaseModel):
    """فیلدهای پایه مکمل"""
    name: str = Field(..., max_length=200)
    name_en: Optional[str] = Field(None, max_length=200)
    brand: Optional[str] = Field(None, max_length=100)
    default_dose: Optional[str] = Field(None, max_length=100)
    dose_unit: Optional[str] = Field(None, max_length=50)
    suggested_time: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    benefits: Optional[str] = None
    side_effects: Optional[str] = None
    contraindications: Optional[str] = None
    is_prescription: bool = False


class SupplementCreate(SupplementBase):
    """ایجاد مکمل"""
    category_id: int


class SupplementResponse(SupplementBase):
    """پاسخ مکمل"""
    id: int
    category_id: int
    is_custom: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SupplementWithCategory(SupplementResponse):
    """مکمل با اطلاعات دسته‌بندی"""
    category: SupplementCategoryResponse


class SupplementCategoryWithSupplements(SupplementCategoryResponse):
    """دسته‌بندی با لیست مکمل‌ها"""
    supplements: List[SupplementResponse] = []
