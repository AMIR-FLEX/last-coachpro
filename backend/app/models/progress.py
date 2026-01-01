"""
Progress Record Model
=====================
مدل ثبت پیشرفت
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.athlete import Athlete


class ProgressRecord(Base, TimestampMixin):
    """
    رکورد پیشرفت
    ============
    ثبت دوره‌ای پیشرفت ورزشکار
    """
    __tablename__ = "progress_records"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"), index=True)
    
    # تاریخ ثبت
    recorded_at: Mapped[date] = mapped_column(Date, default=date.today)
    
    # وزن و ترکیب بدنی
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    body_fat_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    muscle_mass: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # رکوردهای قدرتی (1RM)
    squat_1rm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bench_1rm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    deadlift_1rm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ohp_1rm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # سرشانه
    
    # رکوردهای هوازی
    cardio_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # دقیقه
    cardio_distance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # کیلومتر
    resting_heart_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # ضربان استراحت
    
    # انرژی و احساس
    energy_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-10
    sleep_quality: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-10
    stress_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-10
    soreness_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-10 کوفتگی
    
    # پیروی از برنامه
    training_adherence: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # درصد پیروی از برنامه تمرین
    diet_adherence: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # درصد پیروی از رژیم
    
    # یادداشت و عکس
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # عکس پیشرفت
    
    # روابط
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="progress_records")
    
    def __repr__(self) -> str:
        return f"<ProgressRecord(id={self.id}, athlete_id={self.athlete_id}, date={self.recorded_at})>"
