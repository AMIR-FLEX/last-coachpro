"""
API Dependencies
================
وابستگی‌های مشترک API
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_token


# HTTP Bearer برای دریافت توکن از هدر
security = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency برای دریافت session دیتابیس
    
    این تابع اطمینان می‌دهد که:
    - Session همیشه بسته می‌شود حتی در صورت خطا
    - Transaction ها به درستی commit یا rollback می‌شوند
    
    Note: این تابع duplicate است با backend/app/db/session.py
    برای سازگاری با کد موجود نگه داشته شده است.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> User:
    """
    دریافت کاربر فعلی از توکن
    
    Raises:
        HTTPException: اگر توکن نامعتبر باشد
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن احراز هویت ارسال نشده",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = verify_token(token, "access")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن نامعتبر یا منقضی شده",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن نامعتبر",
        )
    
    user = db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="کاربر یافت نشد",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است",
        )
    
    return user


def get_current_user_optional(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    دریافت کاربر فعلی (اختیاری)
    برای endpoint هایی که هم با و هم بدون توکن کار می‌کنند
    """
    if not credentials:
        return None
    
    try:
        return get_current_user(db, credentials)
    except HTTPException:
        return None


def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    بررسی دسترسی ادمین
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی فقط برای مدیران سیستم",
        )
    return current_user
