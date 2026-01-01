"""
Supplement Plan Models
======================
مدل‌های برنامه مکمل
"""

from sqlalchemy import String, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.athlete import Athlete
    from app.models.supplement import Supplement


class SupplementPlan(Base, TimestampMixin):
    """
    برنامه مکمل
    ===========
    لیست مکمل‌های تجویز شده برای یک ورزشکار
    """
    __tablename__ = "supplement_plans"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"), index=True)
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(200), default="نسخه مکمل")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # یادداشت‌های کلی
    general_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # وضعیت
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="supplement_plans")
    items: Mapped[List["SupplementPlanItem"]] = relationship(
        "SupplementPlanItem",
        back_populates="supplement_plan",
        cascade="all, delete-orphan",
        order_by="SupplementPlanItem.order"
    )
    
    def __repr__(self) -> str:
        return f"<SupplementPlan(id={self.id}, athlete_id={self.athlete_id})>"


class SupplementPlanItem(Base, TimestampMixin):
    """
    آیتم مکمل
    =========
    یک مکمل در نسخه مکمل
    """
    __tablename__ = "supplement_plan_items"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    supplement_plan_id: Mapped[int] = mapped_column(ForeignKey("supplement_plans.id", ondelete="CASCADE"), index=True)
    supplement_id: Mapped[Optional[int]] = mapped_column(ForeignKey("supplements.id", ondelete="SET NULL"), nullable=True)
    
    # ترتیب در لیست
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    # نام مکمل (برای مکمل‌های سفارشی)
    custom_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # دوز تجویزی
    dose: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # "30 گرم" یا "2 عدد"
    
    # زمان مصرف
    timing: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # "صبح ناشتا" یا "بعد تمرین"
    
    # دستورالعمل خاص
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # یادداشت
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # روابط
    supplement_plan: Mapped["SupplementPlan"] = relationship("SupplementPlan", back_populates="items")
    supplement: Mapped[Optional["Supplement"]] = relationship("Supplement")
    
    @property
    def display_name(self) -> str:
        """نام نمایشی مکمل"""
        if self.supplement:
            return self.supplement.name
        return self.custom_name or "بدون نام"
    
    def __repr__(self) -> str:
        return f"<SupplementPlanItem(id={self.id}, name={self.display_name}, dose={self.dose})>"
