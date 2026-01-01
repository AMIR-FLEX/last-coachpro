"""
Training Plan Schemas
=====================
اسکیماهای برنامه تمرینی
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SetType(str, Enum):
    NORMAL = "normal"
    WARMUP = "warmup"
    DROPSET = "dropset"
    SUPERSET = "superset"
    TRISET = "triset"
    GIANTSET = "giantset"
    REST_PAUSE = "rest_pause"
    CLUSTER = "cluster"


# ===== Workout Item Schemas =====

class WorkoutItemBase(BaseModel):
    """فیلدهای پایه آیتم تمرینی"""
    order: int = 0
    set_type: SetType = SetType.NORMAL
    exercise_id: Optional[int] = None
    custom_name: Optional[str] = Field(None, max_length=200)
    sets: Optional[int] = Field(None, ge=1, le=20)
    reps: Optional[str] = Field(None, max_length=50)
    duration_minutes: Optional[int] = Field(None, ge=1, le=180)
    intensity: Optional[str] = Field(None, max_length=50)
    rest_seconds: Optional[int] = Field(None, ge=0, le=600)
    tempo: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    superset_group_id: Optional[str] = Field(None, max_length=50)
    secondary_exercise_name: Optional[str] = Field(None, max_length=200)
    tertiary_exercise_name: Optional[str] = Field(None, max_length=200)


class WorkoutItemCreate(WorkoutItemBase):
    """ایجاد آیتم تمرینی"""
    pass


class WorkoutItemResponse(WorkoutItemBase):
    """پاسخ آیتم تمرینی"""
    id: int
    training_day_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Training Day Schemas =====

class TrainingDayBase(BaseModel):
    """فیلدهای پایه روز تمرینی"""
    day_number: int = Field(..., ge=1, le=7)
    name: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    is_rest_day: bool = False


class TrainingDayCreate(TrainingDayBase):
    """ایجاد روز تمرینی"""
    workout_items: List[WorkoutItemCreate] = []


class TrainingDayUpdate(BaseModel):
    """ویرایش روز تمرینی"""
    name: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    is_rest_day: Optional[bool] = None


class TrainingDayResponse(TrainingDayBase):
    """پاسخ روز تمرینی"""
    id: int
    training_plan_id: int
    workout_items: List[WorkoutItemResponse] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Training Plan Schemas =====

class TrainingPlanBase(BaseModel):
    """فیلدهای پایه برنامه تمرینی"""
    name: str = Field(default="برنامه تمرینی", max_length=200)
    description: Optional[str] = None
    duration_weeks: Optional[int] = Field(None, ge=1, le=52)
    split_type: Optional[str] = Field(None, max_length=50)


class TrainingPlanCreate(TrainingPlanBase):
    """ایجاد برنامه تمرینی"""
    athlete_id: int
    days: List[TrainingDayCreate] = []


class TrainingPlanUpdate(BaseModel):
    """ویرایش برنامه تمرینی"""
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    duration_weeks: Optional[int] = Field(None, ge=1, le=52)
    split_type: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class TrainingPlanResponse(TrainingPlanBase):
    """پاسخ برنامه تمرینی"""
    id: int
    athlete_id: int
    is_active: bool
    days: List[TrainingDayResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TrainingPlanSummary(BaseModel):
    """خلاصه برنامه تمرینی"""
    id: int
    name: str
    duration_weeks: Optional[int]
    split_type: Optional[str]
    is_active: bool
    total_days: int
    total_exercises: int
    created_at: datetime
    
    class Config:
        from_attributes = True
