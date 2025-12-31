"""
Exercise Service
================
سرویس مدیریت بانک تمرینات
"""

from typing import Optional, List, Set
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_, or_

from app.models.exercise import Exercise, MuscleGroup, ExerciseType
from app.schemas.exercise import ExerciseCreate, MuscleGroupCreate, ExerciseSearch


class ExerciseService:
    """سرویس مدیریت تمرینات"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===== Muscle Groups =====
    
    def get_muscle_group(self, group_id: int) -> Optional[MuscleGroup]:
        """دریافت گروه عضلانی"""
        return self.db.get(MuscleGroup, group_id)
    
    def get_all_muscle_groups(self) -> List[MuscleGroup]:
        """دریافت همه گروه‌های عضلانی"""
        stmt = select(MuscleGroup).order_by(MuscleGroup.sort_order)
        return list(self.db.execute(stmt).scalars().all())
    
    def create_muscle_group(self, group_data: MuscleGroupCreate) -> MuscleGroup:
        """ایجاد گروه عضلانی"""
        group = MuscleGroup(**group_data.model_dump())
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group
    
    def get_groups_with_exercises(self) -> List[MuscleGroup]:
        """دریافت گروه‌های عضلانی با تمرینات"""
        stmt = (
            select(MuscleGroup)
            .options(joinedload(MuscleGroup.exercises))
            .order_by(MuscleGroup.sort_order)
        )
        return list(self.db.execute(stmt).unique().scalars().all())
    
    # ===== Exercises =====
    
    def get_exercise(self, exercise_id: int) -> Optional[Exercise]:
        """دریافت تمرین"""
        return self.db.get(Exercise, exercise_id)
    
    def get_exercises_by_muscle(
        self, 
        muscle_group_id: int,
        exercise_type: Optional[ExerciseType] = None,
        active_only: bool = True
    ) -> List[Exercise]:
        """دریافت تمرینات یک گروه عضلانی"""
        stmt = select(Exercise).where(Exercise.muscle_group_id == muscle_group_id)
        
        if exercise_type:
            stmt = stmt.where(Exercise.type == exercise_type)
        
        if active_only:
            stmt = stmt.where(Exercise.is_active == True)
        
        stmt = stmt.order_by(Exercise.name)
        return list(self.db.execute(stmt).scalars().all())
    
    def create_exercise(self, exercise_data: ExerciseCreate, is_custom: bool = False) -> Exercise:
        """ایجاد تمرین"""
        exercise = Exercise(
            **exercise_data.model_dump(),
            is_custom=is_custom
        )
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        return exercise
    
    def search(self, search_params: ExerciseSearch) -> List[Exercise]:
        """جستجوی تمرینات"""
        stmt = select(Exercise).where(Exercise.is_active == True)
        
        if search_params.query:
            stmt = stmt.where(
                or_(
                    Exercise.name.ilike(f"%{search_params.query}%"),
                    Exercise.name_en.ilike(f"%{search_params.query}%")
                )
            )
        
        if search_params.muscle_group_id:
            stmt = stmt.where(Exercise.muscle_group_id == search_params.muscle_group_id)
        
        if search_params.type:
            stmt = stmt.where(Exercise.type == search_params.type)
        
        if search_params.equipment:
            stmt = stmt.where(Exercise.equipment == search_params.equipment)
        
        if search_params.difficulty:
            stmt = stmt.where(Exercise.difficulty == search_params.difficulty)
        
        if search_params.is_compound is not None:
            stmt = stmt.where(Exercise.is_compound == search_params.is_compound)
        
        if search_params.exclude_risky:
            stmt = stmt.where(Exercise.is_risky == False)
        
        offset = (search_params.page - 1) * search_params.page_size
        stmt = stmt.order_by(Exercise.name).offset(offset).limit(search_params.page_size)
        
        return list(self.db.execute(stmt).scalars().all())
    
    def get_by_type(
        self, 
        exercise_type: ExerciseType,
        limit: int = 50
    ) -> List[Exercise]:
        """دریافت تمرینات بر اساس نوع"""
        stmt = (
            select(Exercise)
            .where(
                and_(
                    Exercise.is_active == True,
                    Exercise.type == exercise_type
                )
            )
            .order_by(Exercise.name)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
    
    def get_compound_exercises(self, limit: int = 30) -> List[Exercise]:
        """دریافت حرکات چندمفصلی"""
        stmt = (
            select(Exercise)
            .where(
                and_(
                    Exercise.is_active == True,
                    Exercise.is_compound == True
                )
            )
            .order_by(Exercise.name)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
    
    def get_safe_exercises(
        self,
        muscle_group_id: Optional[int] = None,
        excluded_exercises: Optional[Set[str]] = None
    ) -> List[Exercise]:
        """دریافت تمرینات امن (غیر پرخطر)"""
        stmt = (
            select(Exercise)
            .where(
                and_(
                    Exercise.is_active == True,
                    Exercise.is_risky == False
                )
            )
        )
        
        if muscle_group_id:
            stmt = stmt.where(Exercise.muscle_group_id == muscle_group_id)
        
        exercises = list(self.db.execute(stmt).scalars().all())
        
        # فیلتر کردن تمرینات ممنوعه
        if excluded_exercises:
            exercises = [
                e for e in exercises 
                if e.name not in excluded_exercises
            ]
        
        return exercises
    
    def count(
        self, 
        muscle_group_id: Optional[int] = None,
        exercise_type: Optional[ExerciseType] = None
    ) -> int:
        """تعداد تمرینات"""
        stmt = select(Exercise).where(Exercise.is_active == True)
        
        if muscle_group_id:
            stmt = stmt.where(Exercise.muscle_group_id == muscle_group_id)
        
        if exercise_type:
            stmt = stmt.where(Exercise.type == exercise_type)
        
        return len(list(self.db.execute(stmt).scalars().all()))
    
    def bulk_create(self, exercises_data: List[dict], muscle_group_id: int) -> int:
        """ایجاد چندین تمرین"""
        count = 0
        for data in exercises_data:
            exercise = Exercise(
                muscle_group_id=muscle_group_id,
                name=data.get("name"),
                name_en=data.get("name_en"),
                type=ExerciseType(data.get("type", "resistance")),
                is_compound=data.get("is_compound", False),
                is_risky=data.get("is_risky", False),
                description=data.get("description"),
            )
            self.db.add(exercise)
            count += 1
        
        self.db.commit()
        return count
