"""
Diet Service
============
سرویس مدیریت برنامه‌های غذایی
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_

from app.models.diet import DietPlan, DietItem, MealType
from app.models.food import Food
from app.schemas.diet import (
    DietPlanCreate, DietPlanUpdate,
    DietItemCreate, MacroSummary
)


class DietService:
    """سرویس مدیریت برنامه‌های غذایی"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===== Diet Plans =====
    
    def get_plan(self, plan_id: int) -> Optional[DietPlan]:
        """دریافت برنامه غذایی با جزئیات"""
        stmt = (
            select(DietPlan)
            .options(joinedload(DietPlan.items))
            .where(DietPlan.id == plan_id)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def get_plans_by_athlete(
        self, 
        athlete_id: int,
        active_only: bool = False
    ) -> List[DietPlan]:
        """دریافت برنامه‌های غذایی یک شاگرد"""
        stmt = select(DietPlan).where(DietPlan.athlete_id == athlete_id)
        
        if active_only:
            stmt = stmt.where(DietPlan.is_active == True)
        
        stmt = stmt.order_by(DietPlan.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())
    
    def get_active_plan(self, athlete_id: int) -> Optional[DietPlan]:
        """دریافت برنامه فعال شاگرد"""
        stmt = (
            select(DietPlan)
            .options(joinedload(DietPlan.items))
            .where(
                and_(
                    DietPlan.athlete_id == athlete_id,
                    DietPlan.is_active == True
                )
            )
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def create_plan(self, plan_data: DietPlanCreate) -> DietPlan:
        """ایجاد برنامه غذایی"""
        # غیرفعال کردن برنامه‌های قبلی
        self._deactivate_athlete_plans(plan_data.athlete_id)
        
        plan = DietPlan(
            athlete_id=plan_data.athlete_id,
            name=plan_data.name,
            description=plan_data.description,
            target_calories=plan_data.target_calories,
            target_protein=plan_data.target_protein,
            target_carbs=plan_data.target_carbs,
            target_fat=plan_data.target_fat,
            general_notes=plan_data.general_notes,
            is_active=True,
        )
        
        # افزودن آیتم‌ها
        for item_data in plan_data.items:
            item = self._create_item(item_data)
            plan.items.append(item)
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def update_plan(
        self, 
        plan_id: int, 
        plan_data: DietPlanUpdate
    ) -> Optional[DietPlan]:
        """ویرایش برنامه غذایی"""
        plan = self.db.get(DietPlan, plan_id)
        if not plan:
            return None
        
        update_data = plan_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def delete_plan(self, plan_id: int) -> bool:
        """حذف برنامه غذایی"""
        plan = self.db.get(DietPlan, plan_id)
        if not plan:
            return False
        
        self.db.delete(plan)
        self.db.commit()
        return True
    
    def activate_plan(self, plan_id: int) -> Optional[DietPlan]:
        """فعال کردن یک برنامه"""
        plan = self.db.get(DietPlan, plan_id)
        if not plan:
            return None
        
        self._deactivate_athlete_plans(plan.athlete_id)
        
        plan.is_active = True
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def _deactivate_athlete_plans(self, athlete_id: int) -> None:
        """غیرفعال کردن همه برنامه‌های شاگرد"""
        stmt = (
            select(DietPlan)
            .where(
                and_(
                    DietPlan.athlete_id == athlete_id,
                    DietPlan.is_active == True
                )
            )
        )
        plans = self.db.execute(stmt).scalars().all()
        for plan in plans:
            plan.is_active = False
    
    # ===== Diet Items =====
    
    def add_item(self, plan_id: int, item_data: DietItemCreate) -> Optional[DietItem]:
        """افزودن غذا به برنامه"""
        plan = self.db.get(DietPlan, plan_id)
        if not plan:
            return None
        
        # تعیین ترتیب جدید
        max_order = max([i.order for i in plan.items], default=0)
        
        item = self._create_item(item_data)
        item.diet_plan_id = plan_id
        item.order = max_order + 1
        
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def update_item(self, item_id: int, item_data: dict) -> Optional[DietItem]:
        """ویرایش آیتم غذایی"""
        item = self.db.get(DietItem, item_id)
        if not item:
            return None
        
        for field, value in item_data.items():
            if hasattr(item, field):
                setattr(item, field, value)
        
        # بروزرسانی ماکروها
        if "amount" in item_data or "food_id" in item_data:
            item.calculate_macros()
        
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_item(self, item_id: int) -> bool:
        """حذف آیتم غذایی"""
        item = self.db.get(DietItem, item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def _create_item(self, item_data: DietItemCreate) -> DietItem:
        """ایجاد آیتم غذایی (internal)"""
        item = DietItem(
            order=item_data.order,
            meal=item_data.meal,
            food_id=item_data.food_id,
            custom_name=item_data.custom_name,
            amount=item_data.amount,
            unit=item_data.unit,
            notes=item_data.notes,
        )
        
        # محاسبه ماکروها
        if item_data.food_id:
            food = self.db.get(Food, item_data.food_id)
            if food:
                macros = food.calculate_macros(item_data.amount)
                item.calculated_calories = macros["calories"]
                item.calculated_protein = macros["protein"]
                item.calculated_carbs = macros["carbs"]
                item.calculated_fat = macros["fat"]
        elif item_data.custom_calories:
            # ماکروهای دستی برای غذای سفارشی
            item.calculated_calories = item_data.custom_calories
            item.calculated_protein = item_data.custom_protein or 0
            item.calculated_carbs = item_data.custom_carbs or 0
            item.calculated_fat = item_data.custom_fat or 0
        
        return item
    
    def reorder_items(self, plan_id: int, item_ids: List[int]) -> bool:
        """مرتب‌سازی مجدد آیتم‌ها"""
        plan = self.db.get(DietPlan, plan_id)
        if not plan:
            return False
        
        for order, item_id in enumerate(item_ids):
            item = self.db.get(DietItem, item_id)
            if item and item.diet_plan_id == plan_id:
                item.order = order
        
        self.db.commit()
        return True
    
    # ===== Calculations =====
    
    def calculate_plan_macros(self, plan_id: int) -> MacroSummary:
        """محاسبه مجموع ماکروهای برنامه"""
        plan = self.get_plan(plan_id)
        if not plan:
            return MacroSummary()
        
        totals = MacroSummary(
            target_calories=plan.target_calories,
            target_protein=plan.target_protein,
            target_carbs=plan.target_carbs,
            target_fat=plan.target_fat,
        )
        
        for item in plan.items:
            totals.calories += item.calculated_calories or 0
            totals.protein += item.calculated_protein or 0
            totals.carbs += item.calculated_carbs or 0
            totals.fat += item.calculated_fat or 0
        
        return totals
    
    def get_items_by_meal(self, plan_id: int, meal: MealType) -> List[DietItem]:
        """دریافت آیتم‌های یک وعده"""
        stmt = (
            select(DietItem)
            .where(
                and_(
                    DietItem.diet_plan_id == plan_id,
                    DietItem.meal == meal
                )
            )
            .order_by(DietItem.order)
        )
        return list(self.db.execute(stmt).scalars().all())
    
    def get_meal_summary(self, plan_id: int) -> List[dict]:
        """خلاصه وعده‌ها"""
        plan = self.get_plan(plan_id)
        if not plan:
            return []
        
        meals_summary = {}
        for item in plan.items:
            meal = item.meal.value
            if meal not in meals_summary:
                meals_summary[meal] = {
                    "meal": meal,
                    "items_count": 0,
                    "calories": 0,
                    "protein": 0,
                    "carbs": 0,
                    "fat": 0,
                }
            
            meals_summary[meal]["items_count"] += 1
            meals_summary[meal]["calories"] += item.calculated_calories or 0
            meals_summary[meal]["protein"] += item.calculated_protein or 0
            meals_summary[meal]["carbs"] += item.calculated_carbs or 0
            meals_summary[meal]["fat"] += item.calculated_fat or 0
        
        return list(meals_summary.values())
    
    # ===== Statistics =====
    
    def count_plans(self, athlete_id: int) -> int:
        """تعداد برنامه‌های شاگرد"""
        stmt = select(DietPlan).where(DietPlan.athlete_id == athlete_id)
        return len(list(self.db.execute(stmt).scalars().all()))
