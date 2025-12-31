"""
Diet Plan Schemas
=================
اسکیماهای برنامه غذایی
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MealType(str, Enum):
    BREAKFAST = "صبحانه"
    SNACK_1 = "میان وعده ۱"
    LUNCH = "ناهار"
    SNACK_2 = "میان وعده ۲"
    DINNER = "شام"
    SNACK_3 = "میان وعده ۳"
    PRE_WORKOUT = "قبل تمرین"
    POST_WORKOUT = "بعد تمرین"


class MacroSummary(BaseModel):
    """خلاصه ماکروها"""
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0
    fiber: float = 0
    
    # اهداف (اختیاری)
    target_calories: Optional[int] = None
    target_protein: Optional[int] = None
    target_carbs: Optional[int] = None
    target_fat: Optional[int] = None
    
    @property
    def calories_percentage(self) -> Optional[float]:
        """درصد کالری مصرفی از هدف"""
        if self.target_calories:
            return round((self.calories / self.target_calories) * 100, 1)
        return None


# ===== Diet Item Schemas =====

class DietItemBase(BaseModel):
    """فیلدهای پایه آیتم غذایی"""
    order: int = 0
    meal: MealType
    food_id: Optional[int] = None
    custom_name: Optional[str] = Field(None, max_length=200)
    amount: float = Field(default=100, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class DietItemCreate(DietItemBase):
    """ایجاد آیتم غذایی"""
    # می‌تونیم ماکروها رو برای غذاهای سفارشی دستی وارد کنیم
    custom_calories: Optional[float] = None
    custom_protein: Optional[float] = None
    custom_carbs: Optional[float] = None
    custom_fat: Optional[float] = None


class DietItemResponse(DietItemBase):
    """پاسخ آیتم غذایی"""
    id: int
    diet_plan_id: int
    calculated_calories: Optional[float] = None
    calculated_protein: Optional[float] = None
    calculated_carbs: Optional[float] = None
    calculated_fat: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Diet Plan Schemas =====

class DietPlanBase(BaseModel):
    """فیلدهای پایه برنامه غذایی"""
    name: str = Field(default="برنامه غذایی", max_length=200)
    description: Optional[str] = None
    target_calories: Optional[int] = Field(None, ge=500, le=10000)
    target_protein: Optional[int] = Field(None, ge=0, le=500)
    target_carbs: Optional[int] = Field(None, ge=0, le=1000)
    target_fat: Optional[int] = Field(None, ge=0, le=500)
    general_notes: Optional[str] = None


class DietPlanCreate(DietPlanBase):
    """ایجاد برنامه غذایی"""
    athlete_id: int
    items: List[DietItemCreate] = []


class DietPlanUpdate(BaseModel):
    """ویرایش برنامه غذایی"""
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    target_calories: Optional[int] = Field(None, ge=500, le=10000)
    target_protein: Optional[int] = Field(None, ge=0, le=500)
    target_carbs: Optional[int] = Field(None, ge=0, le=1000)
    target_fat: Optional[int] = Field(None, ge=0, le=500)
    general_notes: Optional[str] = None
    is_active: Optional[bool] = None


class DietPlanResponse(DietPlanBase):
    """پاسخ برنامه غذایی"""
    id: int
    athlete_id: int
    is_active: bool
    items: List[DietItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # ماکروهای کل محاسبه شده
    total_macros: Optional[MacroSummary] = None
    
    class Config:
        from_attributes = True


class DietPlanSummary(BaseModel):
    """خلاصه برنامه غذایی"""
    id: int
    name: str
    target_calories: Optional[int]
    is_active: bool
    total_items: int
    actual_calories: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class MealSummary(BaseModel):
    """خلاصه یک وعده"""
    meal: MealType
    items: List[DietItemResponse]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
