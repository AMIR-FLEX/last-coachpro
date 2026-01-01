"""
Supplement Models
=================
مدل‌های بانک مکمل‌ها
"""

from sqlalchemy import String, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from app.db.base import Base, TimestampMixin


class SupplementCategory(Base, TimestampMixin):
    """
    دسته‌بندی مکمل‌ها
    =================
    مثال: پروتئین‌ها، کراتین، ویتامین‌ها و...
    """
    __tablename__ = "supplement_categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(100))           # پروتئین‌ها
    name_en: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Proteins
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)      # 💊
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    supplements: Mapped[List["Supplement"]] = relationship(
        "Supplement",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<SupplementCategory(id={self.id}, name={self.name})>"


class Supplement(Base, TimestampMixin):
    """
    بانک مکمل‌ها
    ============
    شامل اطلاعات کامل مکمل‌های ورزشی و دارویی
    """
    __tablename__ = "supplements"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("supplement_categories.id"), index=True)
    
    # اطلاعات پایه
    name: Mapped[str] = mapped_column(String(200))           # وی پروتئین
    name_en: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # Whey Protein
    brand: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)    # برند
    
    # دوز پیشنهادی
    default_dose: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 30 گرم
    dose_unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)      # گرم، عدد، cc
    
    # زمان مصرف پیشنهادی
    suggested_time: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # بعد از تمرین
    
    # توضیحات
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    benefits: Mapped[Optional[str]] = mapped_column(Text, nullable=True)      # مزایا
    side_effects: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # عوارض
    contraindications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # موارد منع مصرف
    
    # متادیتا
    is_prescription: Mapped[bool] = mapped_column(Boolean, default=False)  # نیاز به نسخه پزشک
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # روابط
    category: Mapped["SupplementCategory"] = relationship(
        "SupplementCategory", 
        back_populates="supplements"
    )
    
    def __repr__(self) -> str:
        return f"<Supplement(id={self.id}, name={self.name})>"
