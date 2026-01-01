"""
User Schemas
============
اسکیماهای کاربر (مربی)
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """فیلدهای پایه کاربر"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    theme: str = "dark"
    language: str = "fa"


class UserCreate(UserBase):
    """اسکیما ایجاد کاربر"""
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """اسکیما ویرایش کاربر"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    theme: Optional[str] = None
    language: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class UserResponse(UserBase):
    """اسکیما پاسخ کاربر"""
    id: int
    is_active: bool
    is_superuser: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """اسکیما ورود"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """اسکیما توکن"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """محتوای توکن"""
    sub: int  # user_id
    exp: datetime
    type: str = "access"  # access یا refresh
