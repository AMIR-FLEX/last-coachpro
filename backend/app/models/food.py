"""
Food Models
===========
مدل‌های بانک غذاها
"""

from sqlalchemy import String, Float, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from app.db.base import Base, TimestampMixin


class FoodCategory(Base, TimestampMixin):
    """
    دسته‌بندی غذاها
    ================
    مثال: منابع پروتئین، منابع کربوهیدرات، سبزیجات و...
    """
    __tablename__ = "food_categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(100))           # منابع پروتئین
    name_en: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Protein Sources
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)      # 🥩
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    foods: Mapped[List["Food"]] = relationship(
        "Food",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<FoodCategory(id={self.id}, name={self.name})>"


class Food(Base, TimestampMixin):
    """
    بانک غذاها
    ===========
    شامل اطلاعات کامل تغذیه‌ای هر غذا
    """
    __tablename__ = "foods"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("food_categories.id"), index=True)
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(200))           # سینه مرغ (پخته)
    name_en: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # Grilled Chicken Breast
    
    # واحد اندازه‌گیری
    unit: Mapped[str] = mapped_column(String(50))            # گرم، عدد، قاشق غذاخوری
    base_amount: Mapped[float] = mapped_column(Float, default=100)  # مقدار پایه برای محاسبه
    
    # ماکروها (به ازای base_amount)
    calories: Mapped[float] = mapped_column(Float)           # کالری
    protein: Mapped[float] = mapped_column(Float, default=0) # پروتئین (گرم)
    carbs: Mapped[float] = mapped_column(Float, default=0)   # کربوهیدرات (گرم)
    fat: Mapped[float] = mapped_column(Float, default=0)     # چربی (گرم)
    
    # ماکروهای تکمیلی (اختیاری)
    fiber: Mapped[Optional[float]] = mapped_column(Float, nullable=True)    # فیبر
    sugar: Mapped[Optional[float]] = mapped_column(Float, nullable=True)    # قند
    sodium: Mapped[Optional[float]] = mapped_column(Float, nullable=True)   # سدیم (mg)
    
    # متادیتا
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)  # غذای سفارشی کاربر
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    category: Mapped["FoodCategory"] = relationship("FoodCategory", back_populates="foods")
    
    def calculate_macros(self, amount: float) -> dict:
        """
        محاسبه ماکروها برای مقدار مشخص
        
        Args:
            amount: مقدار غذا
            
        Returns:
            دیکشنری شامل کالری و ماکروها
        """
        ratio = amount / self.base_amount
        return {
            "calories": round(self.calories * ratio, 1),
            "protein": round(self.protein * ratio, 1),
            "carbs": round(self.carbs * ratio, 1),
            "fat": round(self.fat * ratio, 1),
            "fiber": round((self.fiber or 0) * ratio, 1),
        }
    
    def __repr__(self) -> str:
        return f"<Food(id={self.id}, name={self.name}, cal={self.calories})>"
