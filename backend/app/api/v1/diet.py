"""
Diet Routes
===========
مسیرهای برنامه غذایی
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.diet_service import DietService
from app.services.athlete_service import AthleteService
from app.schemas.diet import (
    DietPlanCreate, DietPlanUpdate, DietPlanResponse,
    DietItemCreate, DietItemResponse, MacroSummary
)
from app.models.user import User

router = APIRouter()


# ===== Diet Plans =====

@router.get("/athlete/{athlete_id}", response_model=List[DietPlanResponse])
def get_athlete_diet_plans(
    athlete_id: int,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت برنامه‌های غذایی یک شاگرد
    """
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = DietService(db)
    return service.get_plans_by_athlete(athlete_id, active_only)


@router.get("/athlete/{athlete_id}/active", response_model=DietPlanResponse)
def get_active_diet_plan(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت برنامه غذایی فعال شاگرد
    """
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = DietService(db)
    plan = service.get_active_plan(athlete_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه فعال یافت نشد")
    
    return plan


@router.post("", response_model=DietPlanResponse, status_code=status.HTTP_201_CREATED)
def create_diet_plan(
    plan_data: DietPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد برنامه غذایی جدید
    """
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(plan_data.athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = DietService(db)
    return service.create_plan(plan_data)


@router.get("/{plan_id}", response_model=DietPlanResponse)
def get_diet_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت جزئیات برنامه غذایی
    """
    service = DietService(db)
    plan = service.get_plan(plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return plan


@router.put("/{plan_id}", response_model=DietPlanResponse)
def update_diet_plan(
    plan_id: int,
    plan_data: DietPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ویرایش برنامه غذایی
    """
    service = DietService(db)
    plan = service.update_plan(plan_id, plan_data)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diet_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف برنامه غذایی
    """
    service = DietService(db)
    
    if not service.delete_plan(plan_id):
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")


@router.post("/{plan_id}/activate", response_model=DietPlanResponse)
def activate_diet_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    فعال کردن برنامه غذایی
    """
    service = DietService(db)
    plan = service.activate_plan(plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return plan


# ===== Macros Calculation =====

@router.get("/{plan_id}/macros", response_model=MacroSummary)
def get_plan_macros(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    محاسبه مجموع ماکروهای برنامه
    """
    service = DietService(db)
    return service.calculate_plan_macros(plan_id)


@router.get("/{plan_id}/meals-summary")
def get_meals_summary(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    خلاصه وعده‌ها
    """
    service = DietService(db)
    return service.get_meal_summary(plan_id)


# ===== Diet Items =====

@router.post("/{plan_id}/items", response_model=DietItemResponse, status_code=status.HTTP_201_CREATED)
def add_diet_item(
    plan_id: int,
    item_data: DietItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    افزودن غذا به برنامه
    """
    service = DietService(db)
    item = service.add_item(plan_id, item_data)
    
    if not item:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diet_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف آیتم غذایی
    """
    service = DietService(db)
    
    if not service.delete_item(item_id):
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")


@router.post("/{plan_id}/reorder")
def reorder_diet_items(
    plan_id: int,
    item_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    مرتب‌سازی مجدد آیتم‌ها
    """
    service = DietService(db)
    
    if not service.reorder_items(plan_id, item_ids):
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return {"message": "ترتیب بروزرسانی شد"}
