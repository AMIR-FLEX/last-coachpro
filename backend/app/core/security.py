"""
Security Module
===============
مدیریت امنیت، JWT و هش پسورد
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings

# تنظیم bcrypt برای هش پسورد
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    هش کردن پسورد
    
    Args:
        password: پسورد خام
        
    Returns:
        پسورد هش شده
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    بررسی صحت پسورد
    
    Args:
        plain_password: پسورد وارد شده
        hashed_password: پسورد هش شده در دیتابیس
        
    Returns:
        True اگر صحیح باشد
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    ایجاد توکن دسترسی JWT
    
    Args:
        subject: شناسه کاربر
        expires_delta: زمان انقضا (اختیاری)
        
    Returns:
        توکن JWT
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc),
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    ایجاد توکن رفرش
    
    Args:
        subject: شناسه کاربر
        expires_delta: زمان انقضا (اختیاری)
        
    Returns:
        توکن رفرش JWT
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    اعتبارسنجی و رمزگشایی توکن
    
    Args:
        token: توکن JWT
        token_type: نوع توکن (access یا refresh)
        
    Returns:
        محتوای توکن یا None در صورت نامعتبر بودن
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # بررسی نوع توکن
        if payload.get("type") != token_type:
            return None
            
        # بررسی انقضا
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) > exp_datetime:
                return None
        
        return payload
        
    except JWTError:
        return None


def decode_token(token: str) -> Optional[int]:
    """
    استخراج user_id از توکن
    
    Args:
        token: توکن JWT
        
    Returns:
        شناسه کاربر یا None
    """
    payload = verify_token(token, "access")
    if payload:
        try:
            return int(payload.get("sub"))
        except (ValueError, TypeError):
            return None
    return None
