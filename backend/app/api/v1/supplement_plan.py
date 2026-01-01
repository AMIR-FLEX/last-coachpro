"""
Supplement Plan Routes
======================
مسیرهای برنامه مکمل
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.supplement_plan_service import SupplementPlanService
from app.services.athlete_service import AthleteService
from app.schemas.supplement_plan import (
    SupplementPlanCreate, SupplementPlanUpdate, SupplementPlanResponse,
    SupplementPlanItemCreate, SupplementPlanItemResponse
)
from app.models.user import User

router = APIRouter()


@router.get("/athlete/{athlete_id}", response_model=List[SupplementPlanResponse])
def get_athlete_supplement_plans(
    athlete_id: int,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت برنامه‌های مکمل یک شاگرد"""
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = SupplementPlanService(db)
    return service.get_plans_by_athlete(athlete_id, active_only)


@router.get("/athlete/{athlete_id}/active", response_model=SupplementPlanResponse)
def get_active_supplement_plan(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت برنامه فعال شاگرد"""
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = SupplementPlanService(db)
    plan = service.get_active_plan(athlete_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه فعال یافت نشد")
    
    return plan


@router.post("", response_model=SupplementPlanResponse, status_code=status.HTTP_201_CREATED)
def create_supplement_plan(
    plan_data: SupplementPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ایجاد برنامه مکمل جدید"""
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(plan_data.athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = SupplementPlanService(db)
    return service.create_plan(plan_data)


@router.put("/{plan_id}", response_model=SupplementPlanResponse)
def update_supplement_plan(
    plan_id: int,
    plan_data: SupplementPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ویرایش برنامه مکمل"""
    service = SupplementPlanService(db)
    plan = service.update_plan(plan_id, plan_data)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return plan


@router.post("/{plan_id}/items", response_model=SupplementPlanItemResponse, status_code=status.HTTP_201_CREATED)
def add_supplement_item(
    plan_id: int,
    item_data: SupplementPlanItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """افزودن مکمل به برنامه"""
    service = SupplementPlanService(db)
    item = service.add_item(plan_id, item_data)
    
    if not item:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplement_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف آیتم مکمل"""
    service = SupplementPlanService(db)
    
    if not service.delete_item(item_id):
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")

