"""
Exercise Schemas
================
اسکیماهای تمرین
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ExerciseType(str, Enum):
    RESISTANCE = "resistance"
    CARDIO = "cardio"
    CORRECTIVE = "corrective"
    WARMUP = "warmup"
    COOLDOWN = "cooldown"
    STRETCHING = "stretching"
    PLYOMETRIC = "plyometric"


class Equipment(str, Enum):
    BARBELL = "barbell"
    DUMBBELL = "dumbbell"
    CABLE = "cable"
    MACHINE = "machine"
    BODYWEIGHT = "bodyweight"
    KETTLEBELL = "kettlebell"
    RESISTANCE_BAND = "band"
    SMITH_MACHINE = "smith"
    TRX = "trx"
    OTHER = "other"


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# ===== Muscle Group Schemas =====

class MuscleGroupBase(BaseModel):
    """فیلدهای پایه گروه عضلانی"""
    name: str = Field(..., max_length=100)
    name_en: Optional[str] = Field(None, max_length=100)
    icon: Optional[str] = Field(None, max_length=50)
    body_region: Optional[str] = Field(None, max_length=50)
    sort_order: int = 0


class MuscleGroupCreate(MuscleGroupBase):
    """ایجاد گروه عضلانی"""
    pass


class MuscleGroupResponse(MuscleGroupBase):
    """پاسخ گروه عضلانی"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Exercise Schemas =====

class ExerciseBase(BaseModel):
    """فیلدهای پایه تمرین"""
    name: str = Field(..., max_length=200)
    name_en: Optional[str] = Field(None, max_length=200)
    type: ExerciseType = ExerciseType.RESISTANCE
    equipment: Optional[Equipment] = None
    difficulty: Optional[Difficulty] = None
    is_compound: bool = False
    is_unilateral: bool = False
    is_risky: bool = False
    secondary_muscles: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    instructions: Optional[str] = None
    tips: Optional[str] = None
    video_url: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)


class ExerciseCreate(ExerciseBase):
    """ایجاد تمرین"""
    muscle_group_id: Optional[int] = None


class ExerciseResponse(ExerciseBase):
    """پاسخ تمرین"""
    id: int
    muscle_group_id: Optional[int] = None
    is_custom: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ExerciseWithMuscleGroup(ExerciseResponse):
    """تمرین با اطلاعات گروه عضلانی"""
    muscle_group: Optional[MuscleGroupResponse] = None


class ExerciseSearch(BaseModel):
    """جستجوی تمرین"""
    query: Optional[str] = None
    muscle_group_id: Optional[int] = None
    type: Optional[ExerciseType] = None
    equipment: Optional[Equipment] = None
    difficulty: Optional[Difficulty] = None
    is_compound: Optional[bool] = None
    exclude_risky: bool = False
    page: int = 1
    page_size: int = 20


class MuscleGroupWithExercises(MuscleGroupResponse):
    """گروه عضلانی با لیست تمرینات"""
    exercises: List[ExerciseResponse] = []
