"""
User Routes
===========
مسیرهای مدیریت کاربران
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserUpdate, UserResponse
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    دریافت پروفایل خودم
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ویرایش پروفایل خودم
    """
    service = UserService(db)
    
    try:
        user = service.update(current_user.id, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats")
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    آمار داشبورد مربی
    """
    from app.services.athlete_service import AthleteService
    
    athlete_service = AthleteService(db)
    
    total_athletes = athlete_service.count_by_coach(current_user.id)
    active_athletes = athlete_service.count_by_coach(current_user.id, active_only=True)
    
    return {
        "total_athletes": total_athletes,
        "active_athletes": active_athletes,
        "inactive_athletes": total_athletes - active_athletes,
    }
