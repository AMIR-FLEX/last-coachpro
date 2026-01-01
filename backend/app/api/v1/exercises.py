"""
Exercise Routes
===============
مسیرهای بانک تمرینات
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_optional
from app.services.exercise_service import ExerciseService
from app.schemas.exercise import (
    MuscleGroupResponse, MuscleGroupWithExercises,
    ExerciseCreate, ExerciseResponse, ExerciseSearch,
    ExerciseType, Equipment, Difficulty
)
from app.models.user import User

router = APIRouter()


@router.get("/muscle-groups", response_model=List[MuscleGroupResponse])
def get_muscle_groups(
    db: Session = Depends(get_db),
):
    """
    دریافت لیست گروه‌های عضلانی
    """
    service = ExerciseService(db)
    return service.get_all_muscle_groups()


@router.get("/muscle-groups/with-exercises", response_model=List[MuscleGroupWithExercises])
def get_muscle_groups_with_exercises(
    db: Session = Depends(get_db),
):
    """
    دریافت گروه‌های عضلانی به همراه تمرینات
    """
    service = ExerciseService(db)
    return service.get_groups_with_exercises()


@router.get("/search", response_model=List[ExerciseResponse])
def search_exercises(
    q: Optional[str] = None,
    muscle_group_id: Optional[int] = None,
    type: Optional[ExerciseType] = None,
    equipment: Optional[Equipment] = None,
    difficulty: Optional[Difficulty] = None,
    is_compound: Optional[bool] = None,
    exclude_risky: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    جستجوی تمرینات
    """
    service = ExerciseService(db)
    
    search_params = ExerciseSearch(
        query=q,
        muscle_group_id=muscle_group_id,
        type=type,
        equipment=equipment,
        difficulty=difficulty,
        is_compound=is_compound,
        exclude_risky=exclude_risky,
        page=page,
        page_size=page_size
    )
    
    return service.search(search_params)


@router.get("/compound", response_model=List[ExerciseResponse])
def get_compound_exercises(
    limit: int = Query(30, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    دریافت حرکات چندمفصلی
    """
    service = ExerciseService(db)
    return service.get_compound_exercises(limit)


@router.get("/by-type/{exercise_type}", response_model=List[ExerciseResponse])
def get_exercises_by_type(
    exercise_type: ExerciseType,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    دریافت تمرینات بر اساس نوع
    """
    service = ExerciseService(db)
    return service.get_by_type(exercise_type, limit)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
):
    """
    دریافت اطلاعات یک تمرین
    """
    service = ExerciseService(db)
    exercise = service.get_exercise(exercise_id)
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="تمرین یافت نشد"
        )
    
    return exercise


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_custom_exercise(
    exercise_data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    ایجاد تمرین سفارشی
    """
    service = ExerciseService(db)
    return service.create_exercise(exercise_data, is_custom=True)


@router.get("/muscle-group/{muscle_group_id}", response_model=List[ExerciseResponse])
def get_exercises_by_muscle(
    muscle_group_id: int,
    type: Optional[ExerciseType] = None,
    db: Session = Depends(get_db),
):
    """
    دریافت تمرینات یک گروه عضلانی
    """
    service = ExerciseService(db)
    return service.get_exercises_by_muscle(muscle_group_id, type)
