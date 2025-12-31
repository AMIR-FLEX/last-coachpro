"""
Athlete Model
=============
مدل شاگرد (ورزشکار)
"""

from sqlalchemy import String, Integer, Float, Boolean, Text, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date
import enum

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.training import TrainingPlan
    from app.models.diet import DietPlan
    from app.models.supplement_plan import SupplementPlan
    from app.models.progress import ProgressRecord


class Gender(str, enum.Enum):
    """جنسیت"""
    MALE = "male"
    FEMALE = "female"


class Goal(str, enum.Enum):
    """هدف ورزشی"""
    BULK = "bulk"           # افزایش حجم
    CUT = "cut"             # کاهش چربی
    MAINTAIN = "maintain"   # نگهداری
    RECOMP = "recomp"       # بازترکیب بدنی
    STRENGTH = "strength"   # افزایش قدرت
    ENDURANCE = "endurance" # افزایش استقامت


class ActivityLevel(str, enum.Enum):
    """سطح فعالیت روزانه"""
    SEDENTARY = "sedentary"         # بدون فعالیت (کارمند پشت میزی)
    LIGHT = "light"                 # فعالیت سبک (۱-۳ روز ورزش)
    MODERATE = "moderate"           # فعالیت متوسط (۳-۵ روز ورزش)
    ACTIVE = "active"               # فعالیت زیاد (۶-۷ روز ورزش)
    VERY_ACTIVE = "very_active"     # فعالیت خیلی زیاد (ورزشکار حرفه‌ای)


class ExperienceLevel(str, enum.Enum):
    """سطح تجربه تمرینی"""
    BEGINNER = "beginner"           # مبتدی (کمتر از ۱ سال)
    INTERMEDIATE = "intermediate"   # متوسط (۱-۳ سال)
    ADVANCED = "advanced"           # پیشرفته (۳-۵ سال)
    ELITE = "elite"                 # حرفه‌ای (بیش از ۵ سال)


class Athlete(Base, TimestampMixin):
    """
    مدل شاگرد (ورزشکار)
    ===================
    شامل تمام اطلاعات فردی، پزشکی و مالی
    """
    __tablename__ = "athletes"
    
    # شناسه
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[Gender]] = mapped_column(SQLEnum(Gender), nullable=True)
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # cm
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # kg
    
    # اطلاعات تماس
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # اطلاعات ورزشی
    goal: Mapped[Optional[Goal]] = mapped_column(SQLEnum(Goal), nullable=True)
    activity_level: Mapped[Optional[ActivityLevel]] = mapped_column(
        SQLEnum(ActivityLevel), nullable=True
    )
    experience_level: Mapped[Optional[ExperienceLevel]] = mapped_column(
        SQLEnum(ExperienceLevel), nullable=True
    )
    
    # اطلاعات شغلی و سبک زندگی
    job: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sleep_quality: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # اطلاعات پزشکی
    allergies: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # حساسیت غذایی
    medical_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # یادداشت مربی
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # اطلاعات مالی
    subscription_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    subscription_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    subscription_amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # وضعیت
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # آواتار
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # روابط
    coach: Mapped["User"] = relationship("User", back_populates="athletes")
    injuries: Mapped[List["AthleteInjury"]] = relationship(
        "AthleteInjury",
        back_populates="athlete",
        cascade="all, delete-orphan"
    )
    measurements: Mapped[List["AthleteMeasurement"]] = relationship(
        "AthleteMeasurement",
        back_populates="athlete",
        cascade="all, delete-orphan",
        order_by="desc(AthleteMeasurement.recorded_at)"
    )
    training_plans: Mapped[List["TrainingPlan"]] = relationship(
        "TrainingPlan",
        back_populates="athlete",
        cascade="all, delete-orphan"
    )
    diet_plans: Mapped[List["DietPlan"]] = relationship(
        "DietPlan",
        back_populates="athlete",
        cascade="all, delete-orphan"
    )
    supplement_plans: Mapped[List["SupplementPlan"]] = relationship(
        "SupplementPlan",
        back_populates="athlete",
        cascade="all, delete-orphan"
    )
    progress_records: Mapped[List["ProgressRecord"]] = relationship(
        "ProgressRecord",
        back_populates="athlete",
        cascade="all, delete-orphan",
        order_by="desc(ProgressRecord.recorded_at)"
    )
    
    def __repr__(self) -> str:
        return f"<Athlete(id={self.id}, name={self.name}, goal={self.goal})>"


class AthleteInjury(Base, TimestampMixin):
    """
    آسیب‌دیدگی‌های ورزشکار
    ======================
    ثبت تاریخچه آسیب‌ها برای جلوگیری از تجویز حرکات پرخطر
    """
    __tablename__ = "athlete_injuries"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"), index=True)
    
    body_part: Mapped[str] = mapped_column(String(100))  # کمر، زانو، شانه
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # mild, moderate, severe
    is_healed: Mapped[bool] = mapped_column(Boolean, default=False)
    injury_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # روابط
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="injuries")
    
    def __repr__(self) -> str:
        return f"<AthleteInjury(athlete_id={self.athlete_id}, body_part={self.body_part})>"


class AthleteMeasurement(Base):
    """
    اندازه‌گیری‌های آنتروپومتری
    ============================
    ثبت دوره‌ای اندازه‌گیری‌های بدن برای پیگیری پیشرفت
    """
    __tablename__ = "athlete_measurements"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"), index=True)
    
    # تاریخ اندازه‌گیری
    recorded_at: Mapped[date] = mapped_column(Date, default=date.today)
    
    # اندازه‌گیری‌ها (cm)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # وزن (kg)
    body_fat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # درصد چربی
    neck: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    chest: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    shoulders: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    waist: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hip: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    thigh_right: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    thigh_left: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    arm_right: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    arm_left: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    forearm_right: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    forearm_left: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calf_right: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calf_left: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wrist: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # یادداشت
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # روابط
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="measurements")
    
    def __repr__(self) -> str:
        return f"<AthleteMeasurement(athlete_id={self.athlete_id}, date={self.recorded_at})>"
