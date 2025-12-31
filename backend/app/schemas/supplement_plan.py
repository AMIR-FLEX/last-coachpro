"""
Supplement Plan Schemas
=======================
اسکیماهای برنامه مکمل
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ===== Supplement Plan Item Schemas =====

class SupplementPlanItemBase(BaseModel):
    """فیلدهای پایه آیتم مکمل"""
    order: int = 0
    supplement_id: Optional[int] = None
    custom_name: Optional[str] = Field(None, max_length=200)
    dose: Optional[str] = Field(None, max_length=100)
    timing: Optional[str] = Field(None, max_length=200)
    instructions: Optional[str] = None
    notes: Optional[str] = None


class SupplementPlanItemCreate(SupplementPlanItemBase):
    """ایجاد آیتم مکمل"""
    pass


class SupplementPlanItemResponse(SupplementPlanItemBase):
    """پاسخ آیتم مکمل"""
    id: int
    supplement_plan_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Supplement Plan Schemas =====

class SupplementPlanBase(BaseModel):
    """فیلدهای پایه برنامه مکمل"""
    name: str = Field(default="نسخه مکمل", max_length=200)
    description: Optional[str] = None
    general_notes: Optional[str] = None


class SupplementPlanCreate(SupplementPlanBase):
    """ایجاد برنامه مکمل"""
    athlete_id: int
    items: List[SupplementPlanItemCreate] = []


class SupplementPlanUpdate(BaseModel):
    """ویرایش برنامه مکمل"""
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    general_notes: Optional[str] = None
    is_active: Optional[bool] = None


class SupplementPlanResponse(SupplementPlanBase):
    """پاسخ برنامه مکمل"""
    id: int
    athlete_id: int
    is_active: bool
    items: List[SupplementPlanItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SupplementPlanSummary(BaseModel):
    """خلاصه برنامه مکمل"""
    id: int
    name: str
    is_active: bool
    total_items: int
    created_at: datetime
    
    class Config:
        from_attributes = True
