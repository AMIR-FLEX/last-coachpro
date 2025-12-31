"""
Authentication Routes
=====================
مسیرهای احراز هویت
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    ثبت‌نام کاربر جدید
    
    - **email**: ایمیل یکتا
    - **password**: حداقل 6 کاراکتر
    - **full_name**: نام کامل
    """
    service = UserService(db)
    
    try:
        user = service.create(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    ورود به سیستم
    
    - **email**: ایمیل ثبت شده
    - **password**: رمز عبور
    
    Returns:
        توکن دسترسی و رفرش
    """
    service = UserService(db)
    
    user = service.authenticate(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    تمدید توکن با استفاده از رفرش توکن
    """
    payload = verify_token(refresh_token, "refresh")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="رفرش توکن نامعتبر یا منقضی شده",
        )
    
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن نامعتبر",
        )
    
    user = db.get(User, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="کاربر یافت نشد یا غیرفعال است",
        )
    
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    دریافت اطلاعات کاربر فعلی
    """
    return current_user


@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    تغییر رمز عبور
    """
    service = UserService(db)
    
    if not service.change_password(current_user.id, old_password, new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز عبور فعلی اشتباه است"
        )
    
    return {"message": "رمز عبور با موفقیت تغییر کرد"}
