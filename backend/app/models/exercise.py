"""
Exercise Models
===============
مدل‌های بانک تمرینات
"""

from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
import enum

from app.db.base import Base, TimestampMixin


class ExerciseType(str, enum.Enum):
    """نوع تمرین"""
    RESISTANCE = "resistance"       # مقاومتی (وزنه)
    CARDIO = "cardio"               # هوازی
    CORRECTIVE = "corrective"       # اصلاحی
    WARMUP = "warmup"               # گرم کردن
    COOLDOWN = "cooldown"           # سرد کردن
    STRETCHING = "stretching"       # کششی
    PLYOMETRIC = "plyometric"       # پلایومتریک


class Equipment(str, enum.Enum):
    """تجهیزات مورد نیاز"""
    BARBELL = "barbell"             # هالتر
    DUMBBELL = "dumbbell"           # دمبل
    CABLE = "cable"                 # کابل
    MACHINE = "machine"             # دستگاه
    BODYWEIGHT = "bodyweight"       # وزن بدن
    KETTLEBELL = "kettlebell"       # کتل‌بل
    RESISTANCE_BAND = "band"        # کش
    SMITH_MACHINE = "smith"         # اسمیت
    TRX = "trx"                     # تی‌آر‌ایکس
    OTHER = "other"                 # سایر


class Difficulty(str, enum.Enum):
    """سطح سختی"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MuscleGroup(Base, TimestampMixin):
    """
    گروه‌های عضلانی
    ===============
    مثال: سینه، پشت، پا، شانه و...
    """
    __tablename__ = "muscle_groups"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(100))           # سینه
    name_en: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Chest
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)      # 💪
    body_region: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # upper, lower, core
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    
    # روابط
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        back_populates="muscle_group",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<MuscleGroup(id={self.id}, name={self.name})>"


class Exercise(Base, TimestampMixin):
    """
    بانک تمرینات
    ============
    شامل تمام اطلاعات یک حرکت ورزشی
    """
    __tablename__ = "exercises"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    muscle_group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("muscle_groups.id"), 
        nullable=True, 
        index=True
    )
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(200))           # پرس سینه هالتر
    name_en: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # Barbell Bench Press
    
    # نوع و دسته‌بندی
    type: Mapped[ExerciseType] = mapped_column(
        SQLEnum(ExerciseType), 
        default=ExerciseType.RESISTANCE
    )
    equipment: Mapped[Optional[Equipment]] = mapped_column(
        SQLEnum(Equipment), 
        nullable=True
    )
    difficulty: Mapped[Optional[Difficulty]] = mapped_column(
        SQLEnum(Difficulty), 
        nullable=True
    )
    
    # ویژگی‌های حرکت
    is_compound: Mapped[bool] = mapped_column(Boolean, default=False)  # چندمفصلی
    is_unilateral: Mapped[bool] = mapped_column(Boolean, default=False)  # یک‌طرفه
    is_risky: Mapped[bool] = mapped_column(Boolean, default=False)  # پرخطر برای آسیب
    
    # عضلات درگیر ثانویه (لیست جداشده با کاما)
    secondary_muscles: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # راهنما
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tips: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # لینک‌های آموزشی
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # متادیتا
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    muscle_group: Mapped[Optional["MuscleGroup"]] = relationship(
        "MuscleGroup", 
        back_populates="exercises"
    )
    
    def __repr__(self) -> str:
        return f"<Exercise(id={self.id}, name={self.name}, type={self.type})>"
