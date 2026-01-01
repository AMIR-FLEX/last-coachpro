"""
Food Schemas
============
اسکیماهای غذا
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ===== Category Schemas =====

class FoodCategoryBase(BaseModel):
    """فیلدهای پایه دسته‌بندی"""
    name: str = Field(..., max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    icon: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    sort_order: int = 0


class FoodCategoryCreate(FoodCategoryBase):
    """ایجاد دسته‌بندی"""
    pass


class FoodCategoryResponse(FoodCategoryBase):
    """پاسخ دسته‌بندی"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Food Schemas =====

class FoodBase(BaseModel):
    """فیلدهای پایه غذا"""
    name: str = Field(..., max_length=200)
    name_en: Optional[str] = Field(None, max_length=200)
    unit: str = Field(..., max_length=50)
    base_amount: float = Field(default=100, ge=0)
    calories: float = Field(..., ge=0)
    protein: float = Field(default=0, ge=0)
    carbs: float = Field(default=0, ge=0)
    fat: float = Field(default=0, ge=0)
    fiber: Optional[float] = Field(None, ge=0)
    sugar: Optional[float] = Field(None, ge=0)
    sodium: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None


class FoodCreate(FoodBase):
    """ایجاد غذا"""
    category_id: int


class FoodResponse(FoodBase):
    """پاسخ غذا"""
    id: int
    category_id: int
    is_custom: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class FoodWithCategory(FoodResponse):
    """غذا با اطلاعات دسته‌بندی"""
    category: FoodCategoryResponse


class FoodSearch(BaseModel):
    """جستجوی غذا"""
    query: Optional[str] = None
    category_id: Optional[int] = None
    min_protein: Optional[float] = None
    max_calories: Optional[float] = None
    page: int = 1
    page_size: int = 20


class FoodCategoryWithFoods(FoodCategoryResponse):
    """دسته‌بندی با لیست غذاها"""
    foods: List[FoodResponse] = []


class CalculatedMacros(BaseModel):
    """ماکروهای محاسبه شده"""
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float = 0
