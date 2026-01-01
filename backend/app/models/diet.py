"""
Diet Plan Models
================
مدل‌های برنامه غذایی
"""

from sqlalchemy import String, Integer, Float, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
import enum

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.athlete import Athlete
    from app.models.food import Food


class MealType(str, enum.Enum):
    """وعده غذایی"""
    BREAKFAST = "صبحانه"
    SNACK_1 = "میان وعده ۱"
    LUNCH = "ناهار"
    SNACK_2 = "میان وعده ۲"
    DINNER = "شام"
    SNACK_3 = "میان وعده ۳"
    PRE_WORKOUT = "قبل تمرین"
    POST_WORKOUT = "بعد تمرین"


class DietPlan(Base, TimestampMixin):
    """
    برنامه غذایی
    ============
    یک برنامه کامل رژیم غذایی
    """
    __tablename__ = "diet_plans"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"), index=True)
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(200), default="برنامه غذایی")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # اهداف کالری و ماکرو (محاسبه شده یا دستی)
    target_calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_protein: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_carbs: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_fat: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # یادداشت‌های کلی
    general_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # وضعیت
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="diet_plans")
    items: Mapped[List["DietItem"]] = relationship(
        "DietItem",
        back_populates="diet_plan",
        cascade="all, delete-orphan",
        order_by="DietItem.order"
    )
    
    @property
    def total_macros(self) -> dict:
        """محاسبه کل ماکروها"""
        totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        for item in self.items:
            totals["calories"] += item.calculated_calories or 0
            totals["protein"] += item.calculated_protein or 0
            totals["carbs"] += item.calculated_carbs or 0
            totals["fat"] += item.calculated_fat or 0
        return totals
    
    def __repr__(self) -> str:
        return f"<DietPlan(id={self.id}, athlete_id={self.athlete_id}, name={self.name})>"


class DietItem(Base, TimestampMixin):
    """
    آیتم غذایی
    ==========
    یک غذا در برنامه غذایی
    """
    __tablename__ = "diet_items"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    diet_plan_id: Mapped[int] = mapped_column(ForeignKey("diet_plans.id", ondelete="CASCADE"), index=True)
    food_id: Mapped[Optional[int]] = mapped_column(ForeignKey("foods.id", ondelete="SET NULL"), nullable=True)
    
    # ترتیب در لیست
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    # وعده غذایی
    meal: Mapped[MealType] = mapped_column(SQLEnum(MealType))
    
    # نام غذا (برای غذاهای سفارشی)
    custom_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # مقدار
    amount: Mapped[float] = mapped_column(Float, default=100)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # ماکروهای محاسبه شده (کش برای سرعت بیشتر)
    calculated_calories: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calculated_protein: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calculated_carbs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calculated_fat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # یادداشت
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # روابط
    diet_plan: Mapped["DietPlan"] = relationship("DietPlan", back_populates="items")
    food: Mapped[Optional["Food"]] = relationship("Food")
    
    @property
    def display_name(self) -> str:
        """نام نمایشی غذا"""
        if self.food:
            return self.food.name
        return self.custom_name or "بدون نام"
    
    def calculate_macros(self) -> None:
        """محاسبه و ذخیره ماکروها"""
        if self.food:
            macros = self.food.calculate_macros(self.amount)
            self.calculated_calories = macros["calories"]
            self.calculated_protein = macros["protein"]
            self.calculated_carbs = macros["carbs"]
            self.calculated_fat = macros["fat"]
    
    def __repr__(self) -> str:
        return f"<DietItem(id={self.id}, meal={self.meal}, name={self.display_name})>"
