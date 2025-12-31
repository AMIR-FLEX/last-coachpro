"""
Training Routes
===============
مسیرهای برنامه تمرینی
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.training_service import TrainingService
from app.services.athlete_service import AthleteService
from app.schemas.training import (
    TrainingPlanCreate, TrainingPlanUpdate, TrainingPlanResponse,
    TrainingDayCreate, TrainingDayResponse,
    WorkoutItemCreate, WorkoutItemResponse
)
from app.models.user import User

router = APIRouter()


# ===== Training Plans =====

@router.get("/athlete/{athlete_id}", response_model=List[TrainingPlanResponse])
def get_athlete_training_plans(
    athlete_id: int,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت برنامه‌های تمرینی یک شاگرد
    """
    # بررسی دسترسی
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = TrainingService(db)
    return service.get_plans_by_athlete(athlete_id, active_only)


@router.get("/athlete/{athlete_id}/active", response_model=TrainingPlanResponse)
def get_active_training_plan(
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت برنامه فعال شاگرد
    """
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = TrainingService(db)
    plan = service.get_active_plan(athlete_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه فعال یافت نشد")
    
    return plan


@router.post("", response_model=TrainingPlanResponse, status_code=status.HTTP_201_CREATED)
def create_training_plan(
    plan_data: TrainingPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد برنامه تمرینی جدید
    """
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(plan_data.athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=404, detail="شاگرد یافت نشد")
    
    service = TrainingService(db)
    return service.create_plan(plan_data)


@router.get("/{plan_id}", response_model=TrainingPlanResponse)
def get_training_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت جزئیات برنامه تمرینی
    """
    service = TrainingService(db)
    plan = service.get_plan(plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    # بررسی دسترسی
    athlete_service = AthleteService(db)
    athlete = athlete_service.get_by_id(plan.athlete_id, current_user.id)
    if not athlete:
        raise HTTPException(status_code=403, detail="دسترسی ندارید")
    
    return plan


@router.put("/{plan_id}", response_model=TrainingPlanResponse)
def update_training_plan(
    plan_id: int,
    plan_data: TrainingPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ویرایش برنامه تمرینی
    """
    service = TrainingService(db)
    plan = service.update_plan(plan_id, plan_data)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف برنامه تمرینی
    """
    service = TrainingService(db)
    
    if not service.delete_plan(plan_id):
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")


@router.post("/{plan_id}/activate", response_model=TrainingPlanResponse)
def activate_training_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    فعال کردن برنامه تمرینی
    """
    service = TrainingService(db)
    plan = service.activate_plan(plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return plan


# ===== Training Days =====

@router.post("/{plan_id}/days", response_model=TrainingDayResponse, status_code=status.HTTP_201_CREATED)
def add_training_day(
    plan_id: int,
    day_data: TrainingDayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    افزودن روز به برنامه
    """
    service = TrainingService(db)
    day = service.add_day(plan_id, day_data)
    
    if not day:
        raise HTTPException(status_code=404, detail="برنامه یافت نشد")
    
    return day


@router.delete("/days/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_day(
    day_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف روز تمرینی
    """
    service = TrainingService(db)
    
    if not service.delete_day(day_id):
        raise HTTPException(status_code=404, detail="روز یافت نشد")


# ===== Workout Items =====

@router.post("/days/{day_id}/items", response_model=WorkoutItemResponse, status_code=status.HTTP_201_CREATED)
def add_workout_item(
    day_id: int,
    item_data: WorkoutItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    افزودن حرکت به روز تمرینی
    """
    service = TrainingService(db)
    item = service.add_workout_item(day_id, item_data)
    
    if not item:
        raise HTTPException(status_code=404, detail="روز یافت نشد")
    
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف حرکت
    """
    service = TrainingService(db)
    
    if not service.delete_workout_item(item_id):
        raise HTTPException(status_code=404, detail="حرکت یافت نشد")


@router.post("/days/{day_id}/reorder")
def reorder_workout_items(
    day_id: int,
    item_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    مرتب‌سازی مجدد حرکات
    """
    service = TrainingService(db)
    
    if not service.reorder_items(day_id, item_ids):
        raise HTTPException(status_code=404, detail="روز یافت نشد")
    
    return {"message": "ترتیب بروزرسانی شد"}
