"""
Training Plan Models
====================
مدل‌های برنامه تمرینی
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
import enum

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.athlete import Athlete
    from app.models.exercise import Exercise


class SetType(str, enum.Enum):
    """نوع ست"""
    NORMAL = "normal"           # ست عادی
    WARMUP = "warmup"           # ست گرم کردن
    DROPSET = "dropset"         # دراپ‌ست
    SUPERSET = "superset"       # سوپرست
    TRISET = "triset"           # تری‌ست
    GIANTSET = "giantset"       # جاینت‌ست
    REST_PAUSE = "rest_pause"   # رست-پاز
    CLUSTER = "cluster"         # کلاستر


class TrainingPlan(Base, TimestampMixin):
    """
    برنامه تمرینی
    =============
    یک برنامه کامل شامل چند روز تمرینی
    """
    __tablename__ = "training_plans"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"), index=True)
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(200), default="برنامه تمرینی")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # مدت برنامه
    duration_weeks: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # نوع تقسیم‌بندی
    split_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # PPL, Upper/Lower, Full Body
    
    # وضعیت
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="training_plans")
    days: Mapped[List["TrainingDay"]] = relationship(
        "TrainingDay",
        back_populates="training_plan",
        cascade="all, delete-orphan",
        order_by="TrainingDay.day_number"
    )
    
    def __repr__(self) -> str:
        return f"<TrainingPlan(id={self.id}, athlete_id={self.athlete_id}, name={self.name})>"


class TrainingDay(Base, TimestampMixin):
    """
    روز تمرینی
    ==========
    یک روز از برنامه تمرینی
    """
    __tablename__ = "training_days"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    training_plan_id: Mapped[int] = mapped_column(ForeignKey("training_plans.id", ondelete="CASCADE"), index=True)
    
    # شماره روز (۱ تا ۷)
    day_number: Mapped[int] = mapped_column(Integer)
    
    # نام روز (اختیاری)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # روز سینه و جلوبازو
    
    # یادداشت
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # آیا روز استراحت است؟
    is_rest_day: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # روابط
    training_plan: Mapped["TrainingPlan"] = relationship("TrainingPlan", back_populates="days")
    workout_items: Mapped[List["WorkoutItem"]] = relationship(
        "WorkoutItem",
        back_populates="training_day",
        cascade="all, delete-orphan",
        order_by="WorkoutItem.order"
    )
    
    def __repr__(self) -> str:
        return f"<TrainingDay(id={self.id}, day={self.day_number}, name={self.name})>"


class WorkoutItem(Base, TimestampMixin):
    """
    آیتم تمرینی
    ===========
    یک حرکت در برنامه روزانه
    """
    __tablename__ = "workout_items"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    training_day_id: Mapped[int] = mapped_column(ForeignKey("training_days.id", ondelete="CASCADE"), index=True)
    exercise_id: Mapped[Optional[int]] = mapped_column(ForeignKey("exercises.id", ondelete="SET NULL"), nullable=True)
    
    # ترتیب در لیست
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    # نوع ست
    set_type: Mapped[SetType] = mapped_column(SQLEnum(SetType), default=SetType.NORMAL)
    
    # نام حرکت (برای حرکات سفارشی یا وقتی exercise_id نال است)
    custom_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # پارامترهای تمرین
    sets: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reps: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "8-12" یا "تا واماندگی"
    
    # برای تمرینات هوازی
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    intensity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # ضربان قلب یا RPE
    
    # استراحت
    rest_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # تمپو (مثلاً 3-1-2-0)
    tempo: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # یادداشت
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # برای سوپرست/تری‌ست - شناسه گروه
    superset_group_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # حرکات اضافی برای سوپرست (نام حرکت دوم و سوم)
    secondary_exercise_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    tertiary_exercise_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # روابط
    training_day: Mapped["TrainingDay"] = relationship("TrainingDay", back_populates="workout_items")
    exercise: Mapped[Optional["Exercise"]] = relationship("Exercise")
    
    @property
    def display_name(self) -> str:
        """نام نمایشی حرکت"""
        if self.exercise:
            return self.exercise.name
        return self.custom_name or "بدون نام"
    
    def __repr__(self) -> str:
        return f"<WorkoutItem(id={self.id}, exercise={self.display_name}, sets={self.sets})>"
