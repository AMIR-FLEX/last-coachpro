"""
Supplement Plan Service
=======================
سرویس مدیریت برنامه‌های مکمل
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_

from app.models.supplement_plan import SupplementPlan, SupplementPlanItem
from app.schemas.supplement_plan import (
    SupplementPlanCreate, SupplementPlanUpdate,
    SupplementPlanItemCreate
)


class SupplementPlanService:
    """سرویس مدیریت برنامه‌های مکمل"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_plan(self, plan_id: int) -> Optional[SupplementPlan]:
        """دریافت برنامه مکمل با جزئیات"""
        stmt = (
            select(SupplementPlan)
            .options(joinedload(SupplementPlan.items))
            .where(SupplementPlan.id == plan_id)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def get_plans_by_athlete(
        self, 
        athlete_id: int,
        active_only: bool = False
    ) -> List[SupplementPlan]:
        """دریافت برنامه‌های مکمل یک شاگرد"""
        stmt = select(SupplementPlan).where(SupplementPlan.athlete_id == athlete_id)
        
        if active_only:
            stmt = stmt.where(SupplementPlan.is_active == True)
        
        stmt = stmt.order_by(SupplementPlan.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())
    
    def get_active_plan(self, athlete_id: int) -> Optional[SupplementPlan]:
        """دریافت برنامه فعال شاگرد"""
        stmt = (
            select(SupplementPlan)
            .options(joinedload(SupplementPlan.items))
            .where(
                and_(
                    SupplementPlan.athlete_id == athlete_id,
                    SupplementPlan.is_active == True
                )
            )
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def create_plan(self, plan_data: SupplementPlanCreate) -> SupplementPlan:
        """ایجاد برنامه مکمل"""
        self._deactivate_athlete_plans(plan_data.athlete_id)
        
        plan = SupplementPlan(
            athlete_id=plan_data.athlete_id,
            name=plan_data.name,
            description=plan_data.description,
            general_notes=plan_data.general_notes,
            is_active=True,
        )
        
        for item_data in plan_data.items:
            item = SupplementPlanItem(
                order=item_data.order,
                supplement_id=item_data.supplement_id,
                custom_name=item_data.custom_name,
                dose=item_data.dose,
                timing=item_data.timing,
                instructions=item_data.instructions,
                notes=item_data.notes,
            )
            plan.items.append(item)
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def update_plan(
        self, 
        plan_id: int, 
        plan_data: SupplementPlanUpdate
    ) -> Optional[SupplementPlan]:
        """ویرایش برنامه مکمل"""
        plan = self.db.get(SupplementPlan, plan_id)
        if not plan:
            return None
        
        if plan_data.name is not None:
            plan.name = plan_data.name
        if plan_data.description is not None:
            plan.description = plan_data.description
        if plan_data.general_notes is not None:
            plan.general_notes = plan_data.general_notes
        if plan_data.is_active is not None:
            plan.is_active = plan_data.is_active
        
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def delete_plan(self, plan_id: int) -> bool:
        """حذف برنامه مکمل"""
        plan = self.db.get(SupplementPlan, plan_id)
        if not plan:
            return False
        
        self.db.delete(plan)
        self.db.commit()
        return True
    
    def add_item(
        self, 
        plan_id: int, 
        item_data: SupplementPlanItemCreate
    ) -> Optional[SupplementPlanItem]:
        """افزودن آیتم به برنامه"""
        plan = self.db.get(SupplementPlan, plan_id)
        if not plan:
            return None
        
        item = SupplementPlanItem(
            supplement_plan_id=plan_id,
            order=item_data.order,
            supplement_id=item_data.supplement_id,
            custom_name=item_data.custom_name,
            dose=item_data.dose,
            timing=item_data.timing,
            instructions=item_data.instructions,
            notes=item_data.notes,
        )
        
        plan.items.append(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_item(self, item_id: int) -> bool:
        """حذف آیتم"""
        item = self.db.get(SupplementPlanItem, item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def _deactivate_athlete_plans(self, athlete_id: int):
        """غیرفعال کردن برنامه‌های قبلی"""
        plans = self.get_plans_by_athlete(athlete_id, active_only=True)
        for plan in plans:
            plan.is_active = False
        self.db.commit()

