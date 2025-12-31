"""
Database Base
=============
کلاس پایه برای مدل‌های SQLAlchemy
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    """کلاس پایه برای تمام مدل‌ها"""
    pass


class TimestampMixin:
    """
    Mixin برای افزودن فیلدهای زمانی به مدل‌ها
    created_at: زمان ایجاد
    updated_at: زمان آخرین بروزرسانی
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    )
