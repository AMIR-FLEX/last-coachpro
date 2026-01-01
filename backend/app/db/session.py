"""
Database Session
================
مدیریت اتصال و session های دیتابیس
"""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import contextlib

from app.config import settings

# ایجاد Engine با تنظیمات بهینه برای SQLite
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # برای SQLite باید check_same_thread را False کنیم تا در FastAPI کار کند
    connect_args["check_same_thread"] = False
    # فعال‌سازی timeout برای جلوگیری از lock های طولانی
    connect_args["timeout"] = 20  # 20 second timeout

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    connect_args=connect_args,
    pool_pre_ping=True,  # بررسی اتصال قبل از استفاده
    # برای SQLite: poolclass=NullPool بهتر است چون SQLite فایل-based است
    poolclass=None if not settings.DATABASE_URL.startswith("sqlite") else None,
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """تنظیم pragma های SQLite برای عملکرد بهتر"""
    if settings.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_conn.cursor()
        # فعال‌سازی WAL mode برای پشتیبانی از concurrent reads/writes
        cursor.execute("PRAGMA journal_mode=WAL")
        # افزایش timeout برای کاهش خطاهای "database is locked"
        cursor.execute("PRAGMA busy_timeout=20000")  # 20 seconds
        # فعال‌سازی foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON")
        # بهینه‌سازی برای عملکرد بهتر
        cursor.execute("PRAGMA synchronous=NORMAL")  # توازن بین امنیت و عملکرد
        cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()


# ایجاد SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # برای جلوگیری از lazy loading issues
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency برای دریافت session دیتابیس
    استفاده در API routes
    
    این تابع اطمینان می‌دهد که:
    - Session همیشه بسته می‌شود حتی در صورت خطا
    - Transaction ها به درستی commit یا rollback می‌شوند
    
    Example:
        @router.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        # اگر خطایی نبود، commit انجام می‌شود
        db.commit()
    except Exception:
        # در صورت خطا، rollback انجام می‌شود
        db.rollback()
        raise
    finally:
        # همیشه session را بسته می‌کنیم
        db.close()
