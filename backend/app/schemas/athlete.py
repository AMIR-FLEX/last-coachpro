"""
Athlete Schemas
===============
اسکیماهای شاگرد (ورزشکار)
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Goal(str, Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTAIN = "maintain"
    RECOMP = "recomp"
    STRENGTH = "strength"
    ENDURANCE = "endurance"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


# ===== Injury Schemas =====

class InjuryBase(BaseModel):
    """فیلدهای پایه آسیب"""
    body_part: str = Field(..., max_length=100)
    description: Optional[str] = None
    severity: Optional[str] = Field(None, pattern="^(mild|moderate|severe)$")
    is_healed: bool = False
    injury_date: Optional[date] = None


class InjuryCreate(InjuryBase):
    """ایجاد آسیب"""
    pass


class InjuryResponse(InjuryBase):
    """پاسخ آسیب"""
    id: int
    athlete_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ===== Measurement Schemas =====

class MeasurementBase(BaseModel):
    """فیلدهای پایه اندازه‌گیری"""
    recorded_at: date = Field(default_factory=date.today)
    weight: Optional[float] = Field(None, ge=20, le=300)
    body_fat: Optional[float] = Field(None, ge=1, le=60)
    neck: Optional[float] = Field(None, ge=20, le=60)
    chest: Optional[float] = Field(None, ge=50, le=200)
    shoulders: Optional[float] = Field(None, ge=60, le=200)
    waist: Optional[float] = Field(None, ge=40, le=200)
    hip: Optional[float] = Field(None, ge=50, le=200)
    thigh_right: Optional[float] = Field(None, ge=30, le=100)
    thigh_left: Optional[float] = Field(None, ge=30, le=100)
    arm_right: Optional[float] = Field(None, ge=20, le=60)
    arm_left: Optional[float] = Field(None, ge=20, le=60)
    forearm_right: Optional[float] = Field(None, ge=15, le=50)
    forearm_left: Optional[float] = Field(None, ge=15, le=50)
    calf_right: Optional[float] = Field(None, ge=20, le=60)
    calf_left: Optional[float] = Field(None, ge=20, le=60)
    wrist: Optional[float] = Field(None, ge=10, le=30)
    notes: Optional[str] = None


class MeasurementCreate(MeasurementBase):
    """ایجاد اندازه‌گیری"""
    pass


class MeasurementResponse(MeasurementBase):
    """پاسخ اندازه‌گیری"""
    id: int
    athlete_id: int
    
    class Config:
        from_attributes = True


# ===== Athlete Schemas =====

class AthleteBase(BaseModel):
    """فیلدهای پایه شاگرد"""
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=10, le=100)
    gender: Optional[Gender] = None
    height: Optional[float] = Field(None, ge=100, le=250)  # cm
    weight: Optional[float] = Field(None, ge=30, le=300)   # kg
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    goal: Optional[Goal] = None
    activity_level: Optional[ActivityLevel] = None
    experience_level: Optional[ExperienceLevel] = None
    job: Optional[str] = Field(None, max_length=100)
    sleep_quality: Optional[str] = Field(None, max_length=50)
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    notes: Optional[str] = None


class AthleteCreate(AthleteBase):
    """ایجاد شاگرد"""
    injuries: Optional[List[InjuryCreate]] = []
    subscription_start: Optional[date] = None
    subscription_months: Optional[int] = Field(None, ge=1, le=24)
    subscription_amount: Optional[int] = Field(None, ge=0)


class AthleteUpdate(BaseModel):
    """ویرایش شاگرد"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=10, le=100)
    gender: Optional[Gender] = None
    height: Optional[float] = Field(None, ge=100, le=250)
    weight: Optional[float] = Field(None, ge=30, le=300)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    goal: Optional[Goal] = None
    activity_level: Optional[ActivityLevel] = None
    experience_level: Optional[ExperienceLevel] = None
    job: Optional[str] = Field(None, max_length=100)
    sleep_quality: Optional[str] = Field(None, max_length=50)
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
    subscription_start: Optional[date] = None
    subscription_months: Optional[int] = Field(None, ge=1, le=24)
    subscription_amount: Optional[int] = Field(None, ge=0)


class AthleteResponse(AthleteBase):
    """پاسخ شاگرد"""
    id: int
    coach_id: int
    is_active: bool
    avatar_url: Optional[str] = None
    subscription_start: Optional[date] = None
    subscription_months: Optional[int] = None
    subscription_amount: Optional[int] = None
    injuries: List[InjuryResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AthleteListResponse(BaseModel):
    """پاسخ لیست شاگردان (خلاصه)"""
    id: int
    name: str
    age: Optional[int] = None
    goal: Optional[Goal] = None
    is_active: bool
    avatar_url: Optional[str] = None
    subscription_start: Optional[date] = None
    subscription_months: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
