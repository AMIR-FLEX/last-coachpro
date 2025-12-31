"""
Progress Record Schemas
=======================
اسکیماهای ثبت پیشرفت
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class ProgressRecordBase(BaseModel):
    """فیلدهای پایه رکورد پیشرفت"""
    recorded_at: date = Field(default_factory=date.today)
    
    # وزن و ترکیب بدنی
    weight: Optional[float] = Field(None, ge=30, le=300)
    body_fat_percentage: Optional[float] = Field(None, ge=1, le=60)
    muscle_mass: Optional[float] = Field(None, ge=10, le=150)
    
    # رکوردهای قدرتی (1RM)
    squat_1rm: Optional[float] = Field(None, ge=0, le=500)
    bench_1rm: Optional[float] = Field(None, ge=0, le=400)
    deadlift_1rm: Optional[float] = Field(None, ge=0, le=500)
    ohp_1rm: Optional[float] = Field(None, ge=0, le=200)
    
    # رکوردهای هوازی
    cardio_time: Optional[int] = Field(None, ge=0, le=300)  # دقیقه
    cardio_distance: Optional[float] = Field(None, ge=0, le=50)  # کیلومتر
    resting_heart_rate: Optional[int] = Field(None, ge=30, le=120)
    
    # انرژی و احساس (1-10)
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    soreness_level: Optional[int] = Field(None, ge=1, le=10)
    
    # پیروی از برنامه (درصد)
    training_adherence: Optional[int] = Field(None, ge=0, le=100)
    diet_adherence: Optional[int] = Field(None, ge=0, le=100)
    
    # یادداشت و عکس
    notes: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)


class ProgressRecordCreate(ProgressRecordBase):
    """ایجاد رکورد پیشرفت"""
    athlete_id: int


class ProgressRecordResponse(ProgressRecordBase):
    """پاسخ رکورد پیشرفت"""
    id: int
    athlete_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProgressSummary(BaseModel):
    """خلاصه پیشرفت"""
    athlete_id: int
    records_count: int
    
    # آخرین مقادیر
    latest_weight: Optional[float] = None
    latest_body_fat: Optional[float] = None
    
    # تغییرات (نسبت به اولین رکورد)
    weight_change: Optional[float] = None
    body_fat_change: Optional[float] = None
    
    # بهترین رکوردها
    best_squat: Optional[float] = None
    best_bench: Optional[float] = None
    best_deadlift: Optional[float] = None
    
    # میانگین‌ها
    avg_energy: Optional[float] = None
    avg_sleep_quality: Optional[float] = None
    avg_training_adherence: Optional[float] = None
    avg_diet_adherence: Optional[float] = None
