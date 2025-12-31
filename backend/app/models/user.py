"""
User Model (Coach)
==================
مدل کاربر (مربی) سیستم
"""

from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.athlete import Athlete


class User(Base, TimestampMixin):
    """
    مدل کاربر (مربی)
    ================
    هر مربی می‌تواند چندین شاگرد داشته باشد
    """
    __tablename__ = "users"
    
    # شناسه
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # اطلاعات احراز هویت
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # اطلاعات پروفایل
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # تنظیمات
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # تنظیمات نمایش
    theme: Mapped[str] = mapped_column(String(20), default="dark")
    language: Mapped[str] = mapped_column(String(10), default="fa")
    
    # روابط
    athletes: Mapped[List["Athlete"]] = relationship(
        "Athlete",
        back_populates="coach",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.full_name})>"
