"""
Athlete Routes
==============
مسیرهای مدیریت شاگردان
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.athlete_service import AthleteService
from app.schemas.athlete import (
    AthleteCreate, AthleteUpdate, AthleteResponse, AthleteListResponse,
    InjuryCreate, InjuryResponse, MeasurementCreate, MeasurementResponse
)
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[AthleteListResponse])
def get_athletes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت لیست شاگردان
    """
    service = AthleteService(db)
    return service.get_all_by_coach(
        current_user.id, 
        skip=skip, 
        limit=limit,
        active_only=active_only
    )


@router.post("", response_model=AthleteResponse, status_code=status.HTTP_201_CREATED)
def create_athlete(
    athlete_data: AthleteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد شاگرد جدید
    """
    service = AthleteService(db)
    return service.create(current_user.id, athlete_data)


@router.get("/search", response_model=List[AthleteListResponse])
def search_athletes(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    جستجوی شاگردان
    """
    service = AthleteService(db)
    return service.search(current_user.id, q, limit)


@router.get("/{athlete_id}", response_model=AthleteResponse)
def get_athlete(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت اطلاعات یک شاگرد
    """
    service = AthleteService(db)
    athlete = service.get_by_id(athlete_id, current_user.id)
    
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    return athlete


@router.put("/{athlete_id}", response_model=AthleteResponse)
def update_athlete(
    athlete_id: int,
    athlete_data: AthleteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ویرایش شاگرد
    """
    service = AthleteService(db)
    athlete = service.update(athlete_id, athlete_data, current_user.id)
    
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    return athlete


@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_athlete(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف شاگرد
    """
    service = AthleteService(db)
    
    if not service.delete(athlete_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )


@router.post("/{athlete_id}/toggle-active", response_model=AthleteResponse)
def toggle_athlete_active(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    تغییر وضعیت فعال/غیرفعال شاگرد
    """
    service = AthleteService(db)
    athlete = service.toggle_active(athlete_id, current_user.id)
    
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    return athlete


# ===== Nutrition Calculation =====

@router.get("/{athlete_id}/nutrition")
def calculate_athlete_nutrition(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    محاسبه نیازهای تغذیه‌ای شاگرد
    """
    service = AthleteService(db)
    
    # بررسی دسترسی
    athlete = service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    result = service.calculate_nutrition(athlete_id)
    
    if result and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result


# ===== Injuries =====

@router.post("/{athlete_id}/injuries", response_model=InjuryResponse, status_code=status.HTTP_201_CREATED)
def add_injury(
    athlete_id: int,
    injury_data: InjuryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ثبت آسیب‌دیدگی
    """
    service = AthleteService(db)
    
    # بررسی دسترسی
    athlete = service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    injury = service.add_injury(athlete_id, injury_data)
    return injury


@router.delete("/injuries/{injury_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_injury(
    injury_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف آسیب‌دیدگی
    """
    service = AthleteService(db)
    
    if not service.remove_injury(injury_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="آسیب یافت نشد"
        )


# ===== Measurements =====

@router.post("/{athlete_id}/measurements", response_model=MeasurementResponse, status_code=status.HTTP_201_CREATED)
def add_measurement(
    athlete_id: int,
    measurement_data: MeasurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ثبت اندازه‌گیری جدید
    """
    service = AthleteService(db)
    
    # بررسی دسترسی
    athlete = service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    measurement = service.add_measurement(athlete_id, measurement_data)
    return measurement


@router.get("/{athlete_id}/measurements", response_model=List[MeasurementResponse])
def get_measurements(
    athlete_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت تاریخچه اندازه‌گیری‌ها
    """
    service = AthleteService(db)
    
    # بررسی دسترسی
    athlete = service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="شاگرد یافت نشد"
        )
    
    return service.get_measurements(athlete_id, limit)
