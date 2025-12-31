"""
User Service
============
سرویس مدیریت کاربران (مربیان)
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    """سرویس مدیریت کاربران"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """دریافت کاربر با شناسه"""
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """دریافت کاربر با ایمیل"""
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """دریافت لیست کاربران"""
        stmt = select(User).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())
    
    def create(self, user_data: UserCreate) -> User:
        """ایجاد کاربر جدید"""
        # بررسی تکراری نبودن ایمیل
        if self.get_by_email(user_data.email):
            raise ValueError("این ایمیل قبلاً ثبت شده است")
        
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            phone=user_data.phone,
            bio=user_data.bio,
            theme=user_data.theme,
            language=user_data.language,
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """ویرایش کاربر"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # هش کردن پسورد جدید
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # بررسی تکراری نبودن ایمیل جدید
        if "email" in update_data and update_data["email"] != user.email:
            if self.get_by_email(update_data["email"]):
                raise ValueError("این ایمیل قبلاً ثبت شده است")
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """حذف کاربر"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """احراز هویت کاربر"""
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user
    
    def change_password(
        self, 
        user_id: int, 
        old_password: str, 
        new_password: str
    ) -> bool:
        """تغییر پسورد"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        if not verify_password(old_password, user.hashed_password):
            return False
        
        user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """تعداد کل کاربران"""
        stmt = select(User)
        return len(list(self.db.execute(stmt).scalars().all()))
