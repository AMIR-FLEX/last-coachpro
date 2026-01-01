"""
Configuration Settings
======================
تنظیمات اصلی اپلیکیشن
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """تنظیمات اصلی اپلیکیشن"""
    
    # اطلاعات اپلیکیشن
    APP_NAME: str = "FLEX PRO"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "سیستم هوشمند مدیریت مربیگری ورزشی"
    DEBUG: bool = True
    
    # تنظیمات API
    API_V1_PREFIX: str = "/api/v1"
    
    # تنظیمات دیتابیس
    DATABASE_URL: str = "sqlite:///./flexpro.db"
    DATABASE_ECHO: bool = False  # نمایش SQL queries در لاگ
    
    # تنظیمات امنیتی - JWT
    SECRET_KEY: str = "flex-pro-super-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 روز
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # تنظیمات CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",      # Next.js default port
        "http://127.0.0.1:3000",      # Next.js with IP
        "http://localhost:5173",      # Vite default port (for legacy)
        "http://127.0.0.1:5173",      # Vite with IP (for legacy)
    ]
    
    # تنظیمات آپلود فایل
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: list[str] = ["jpg", "jpeg", "png", "gif"]
    UPLOAD_DIR: str = "uploads"
    
    # تنظیمات PDF
    PDF_FONT_PATH: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    دریافت تنظیمات با کش
    برای جلوگیری از خواندن مکرر فایل .env
    """
    return Settings()


# نمونه سراسری تنظیمات
settings = get_settings()
