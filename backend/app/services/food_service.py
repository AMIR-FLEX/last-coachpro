"""
Food Service
============
سرویس مدیریت بانک غذاها
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_, or_

from app.models.food import Food, FoodCategory
from app.schemas.food import FoodCreate, FoodCategoryCreate, FoodSearch


class FoodService:
    """سرویس مدیریت غذاها"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===== Categories =====
    
    def get_category(self, category_id: int) -> Optional[FoodCategory]:
        """دریافت دسته‌بندی"""
        return self.db.get(FoodCategory, category_id)
    
    def get_all_categories(self, active_only: bool = True) -> List[FoodCategory]:
        """دریافت همه دسته‌بندی‌ها"""
        stmt = select(FoodCategory).order_by(FoodCategory.sort_order)
        if active_only:
            stmt = stmt.where(FoodCategory.is_active == True)
        return list(self.db.execute(stmt).scalars().all())
    
    def create_category(self, category_data: FoodCategoryCreate) -> FoodCategory:
        """ایجاد دسته‌بندی"""
        category = FoodCategory(**category_data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_categories_with_foods(self) -> List[FoodCategory]:
        """دریافت دسته‌بندی‌ها با غذاها"""
        stmt = (
            select(FoodCategory)
            .options(joinedload(FoodCategory.foods))
            .where(FoodCategory.is_active == True)
            .order_by(FoodCategory.sort_order)
        )
        return list(self.db.execute(stmt).unique().scalars().all())
    
    # ===== Foods =====
    
    def get_food(self, food_id: int) -> Optional[Food]:
        """دریافت غذا"""
        return self.db.get(Food, food_id)
    
    def get_foods_by_category(
        self, 
        category_id: int, 
        active_only: bool = True
    ) -> List[Food]:
        """دریافت غذاهای یک دسته‌بندی"""
        stmt = select(Food).where(Food.category_id == category_id)
        if active_only:
            stmt = stmt.where(Food.is_active == True)
        stmt = stmt.order_by(Food.name)
        return list(self.db.execute(stmt).scalars().all())
    
    def create_food(self, food_data: FoodCreate, is_custom: bool = False) -> Food:
        """ایجاد غذا"""
        food = Food(
            **food_data.model_dump(),
            is_custom=is_custom
        )
        self.db.add(food)
        self.db.commit()
        self.db.refresh(food)
        return food
    
    def search(self, search_params: FoodSearch) -> List[Food]:
        """جستجوی غذاها"""
        stmt = select(Food).where(Food.is_active == True)
        
        if search_params.query:
            stmt = stmt.where(
                or_(
                    Food.name.ilike(f"%{search_params.query}%"),
                    Food.name_en.ilike(f"%{search_params.query}%")
                )
            )
        
        if search_params.category_id:
            stmt = stmt.where(Food.category_id == search_params.category_id)
        
        if search_params.min_protein:
            stmt = stmt.where(Food.protein >= search_params.min_protein)
        
        if search_params.max_calories:
            stmt = stmt.where(Food.calories <= search_params.max_calories)
        
        offset = (search_params.page - 1) * search_params.page_size
        stmt = stmt.order_by(Food.name).offset(offset).limit(search_params.page_size)
        
        return list(self.db.execute(stmt).scalars().all())
    
    def calculate_macros(self, food_id: int, amount: float) -> Optional[dict]:
        """محاسبه ماکروها برای مقدار مشخص"""
        food = self.get_food(food_id)
        if not food:
            return None
        return food.calculate_macros(amount)
    
    def get_high_protein_foods(self, min_protein: float = 20, limit: int = 20) -> List[Food]:
        """غذاهای با پروتئین بالا"""
        stmt = (
            select(Food)
            .where(
                and_(
                    Food.is_active == True,
                    Food.protein >= min_protein
                )
            )
            .order_by(Food.protein.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
    
    def get_low_calorie_foods(self, max_calories: float = 100, limit: int = 20) -> List[Food]:
        """غذاهای کم‌کالری"""
        stmt = (
            select(Food)
            .where(
                and_(
                    Food.is_active == True,
                    Food.calories <= max_calories
                )
            )
            .order_by(Food.calories)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
    
    def count(self, category_id: Optional[int] = None) -> int:
        """تعداد غذاها"""
        stmt = select(Food).where(Food.is_active == True)
        if category_id:
            stmt = stmt.where(Food.category_id == category_id)
        return len(list(self.db.execute(stmt).scalars().all()))
    
    def bulk_create(self, foods_data: List[dict], category_id: int) -> int:
        """ایجاد چندین غذا"""
        count = 0
        for food_data in foods_data:
            food = Food(
                category_id=category_id,
                name=food_data.get("name"),
                unit=food_data.get("unit", "گرم"),
                base_amount=food_data.get("base_amount", 100),
                calories=food_data.get("calories", 0),
                protein=food_data.get("protein", 0),
                carbs=food_data.get("carbs", 0),
                fat=food_data.get("fat", 0),
                fiber=food_data.get("fiber"),
            )
            self.db.add(food)
            count += 1
        
        self.db.commit()
        return count
