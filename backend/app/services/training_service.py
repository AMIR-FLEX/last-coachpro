"""
Training Service
================
سرویس مدیریت برنامه‌های تمرینی
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_

from app.models.training import TrainingPlan, TrainingDay, WorkoutItem
from app.schemas.training import (
    TrainingPlanCreate, TrainingPlanUpdate,
    TrainingDayCreate, WorkoutItemCreate
)


class TrainingService:
    """سرویس مدیریت برنامه‌های تمرینی"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===== Training Plans =====
    
    def get_plan(self, plan_id: int) -> Optional[TrainingPlan]:
        """دریافت برنامه تمرینی با جزئیات"""
        stmt = (
            select(TrainingPlan)
            .options(
                joinedload(TrainingPlan.days)
                .joinedload(TrainingDay.workout_items)
            )
            .where(TrainingPlan.id == plan_id)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def get_plans_by_athlete(
        self, 
        athlete_id: int,
        active_only: bool = False
    ) -> List[TrainingPlan]:
        """دریافت برنامه‌های تمرینی یک شاگرد"""
        stmt = select(TrainingPlan).where(TrainingPlan.athlete_id == athlete_id)
        
        if active_only:
            stmt = stmt.where(TrainingPlan.is_active == True)
        
        stmt = stmt.order_by(TrainingPlan.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())
    
    def get_active_plan(self, athlete_id: int) -> Optional[TrainingPlan]:
        """دریافت برنامه فعال شاگرد"""
        stmt = (
            select(TrainingPlan)
            .options(
                joinedload(TrainingPlan.days)
                .joinedload(TrainingDay.workout_items)
            )
            .where(
                and_(
                    TrainingPlan.athlete_id == athlete_id,
                    TrainingPlan.is_active == True
                )
            )
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def create_plan(self, plan_data: TrainingPlanCreate) -> TrainingPlan:
        """ایجاد برنامه تمرینی"""
        # غیرفعال کردن برنامه‌های قبلی
        self._deactivate_athlete_plans(plan_data.athlete_id)
        
        plan = TrainingPlan(
            athlete_id=plan_data.athlete_id,
            name=plan_data.name,
            description=plan_data.description,
            duration_weeks=plan_data.duration_weeks,
            split_type=plan_data.split_type,
            is_active=True,
        )
        
        # افزودن روزها
        for day_data in plan_data.days:
            day = self._create_day(day_data)
            plan.days.append(day)
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def update_plan(
        self, 
        plan_id: int, 
        plan_data: TrainingPlanUpdate
    ) -> Optional[TrainingPlan]:
        """ویرایش برنامه تمرینی"""
        plan = self.db.get(TrainingPlan, plan_id)
        if not plan:
            return None
        
        update_data = plan_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def delete_plan(self, plan_id: int) -> bool:
        """حذف برنامه تمرینی"""
        plan = self.db.get(TrainingPlan, plan_id)
        if not plan:
            return False
        
        self.db.delete(plan)
        self.db.commit()
        return True
    
    def activate_plan(self, plan_id: int) -> Optional[TrainingPlan]:
        """فعال کردن یک برنامه"""
        plan = self.db.get(TrainingPlan, plan_id)
        if not plan:
            return None
        
        # غیرفعال کردن برنامه‌های قبلی
        self._deactivate_athlete_plans(plan.athlete_id)
        
        plan.is_active = True
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def _deactivate_athlete_plans(self, athlete_id: int) -> None:
        """غیرفعال کردن همه برنامه‌های شاگرد"""
        stmt = (
            select(TrainingPlan)
            .where(
                and_(
                    TrainingPlan.athlete_id == athlete_id,
                    TrainingPlan.is_active == True
                )
            )
        )
        plans = self.db.execute(stmt).scalars().all()
        for plan in plans:
            plan.is_active = False
    
    # ===== Training Days =====
    
    def get_day(self, day_id: int) -> Optional[TrainingDay]:
        """دریافت روز تمرینی"""
        stmt = (
            select(TrainingDay)
            .options(joinedload(TrainingDay.workout_items))
            .where(TrainingDay.id == day_id)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def add_day(self, plan_id: int, day_data: TrainingDayCreate) -> Optional[TrainingDay]:
        """افزودن روز به برنامه"""
        plan = self.db.get(TrainingPlan, plan_id)
        if not plan:
            return None
        
        day = self._create_day(day_data)
        day.training_plan_id = plan_id
        
        self.db.add(day)
        self.db.commit()
        self.db.refresh(day)
        return day
    
    def update_day(self, day_id: int, day_data: dict) -> Optional[TrainingDay]:
        """ویرایش روز تمرینی"""
        day = self.db.get(TrainingDay, day_id)
        if not day:
            return None
        
        for field, value in day_data.items():
            if hasattr(day, field):
                setattr(day, field, value)
        
        self.db.commit()
        self.db.refresh(day)
        return day
    
    def delete_day(self, day_id: int) -> bool:
        """حذف روز تمرینی"""
        day = self.db.get(TrainingDay, day_id)
        if not day:
            return False
        
        self.db.delete(day)
        self.db.commit()
        return True
    
    def _create_day(self, day_data: TrainingDayCreate) -> TrainingDay:
        """ایجاد روز تمرینی (internal)"""
        day = TrainingDay(
            day_number=day_data.day_number,
            name=day_data.name,
            notes=day_data.notes,
            is_rest_day=day_data.is_rest_day,
        )
        
        for item_data in day_data.workout_items:
            item = WorkoutItem(**item_data.model_dump())
            day.workout_items.append(item)
        
        return day
    
    # ===== Workout Items =====
    
    def add_workout_item(
        self, 
        day_id: int, 
        item_data: WorkoutItemCreate
    ) -> Optional[WorkoutItem]:
        """افزودن حرکت به روز تمرینی"""
        day = self.db.get(TrainingDay, day_id)
        if not day:
            return None
        
        # تعیین ترتیب جدید
        max_order = max([i.order for i in day.workout_items], default=0)
        
        item = WorkoutItem(
            training_day_id=day_id,
            order=max_order + 1,
            **item_data.model_dump(exclude={"order"})
        )
        
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def update_workout_item(
        self, 
        item_id: int, 
        item_data: dict
    ) -> Optional[WorkoutItem]:
        """ویرایش حرکت"""
        item = self.db.get(WorkoutItem, item_id)
        if not item:
            return None
        
        for field, value in item_data.items():
            if hasattr(item, field):
                setattr(item, field, value)
        
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_workout_item(self, item_id: int) -> bool:
        """حذف حرکت"""
        item = self.db.get(WorkoutItem, item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def reorder_items(self, day_id: int, item_ids: List[int]) -> bool:
        """مرتب‌سازی مجدد حرکات"""
        day = self.db.get(TrainingDay, day_id)
        if not day:
            return False
        
        for order, item_id in enumerate(item_ids):
            item = self.db.get(WorkoutItem, item_id)
            if item and item.training_day_id == day_id:
                item.order = order
        
        self.db.commit()
        return True
    
    # ===== Statistics =====
    
    def count_plans(self, athlete_id: int) -> int:
        """تعداد برنامه‌های شاگرد"""
        stmt = select(TrainingPlan).where(TrainingPlan.athlete_id == athlete_id)
        return len(list(self.db.execute(stmt).scalars().all()))
    
    def get_total_exercises_in_plan(self, plan_id: int) -> int:
        """تعداد کل حرکات در برنامه"""
        plan = self.get_plan(plan_id)
        if not plan:
            return 0
        
        total = 0
        for day in plan.days:
            total += len(day.workout_items)
        return total
