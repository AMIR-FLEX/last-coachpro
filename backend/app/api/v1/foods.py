"""
Food Routes
===========
مسیرهای بانک غذاها
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_optional
from app.services.food_service import FoodService
from app.schemas.food import (
    FoodCategoryResponse, FoodCategoryWithFoods,
    FoodCreate, FoodResponse, FoodSearch, CalculatedMacros
)
from app.models.user import User

router = APIRouter()


@router.get("/categories", response_model=List[FoodCategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
):
    """
    دریافت لیست دسته‌بندی‌های غذا
    """
    service = FoodService(db)
    return service.get_all_categories()


@router.get("/categories/with-foods", response_model=List[FoodCategoryWithFoods])
def get_categories_with_foods(
    db: Session = Depends(get_db),
):
    """
    دریافت دسته‌بندی‌ها به همراه غذاها
    """
    service = FoodService(db)
    return service.get_categories_with_foods()


@router.get("/search", response_model=List[FoodResponse])
def search_foods(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    min_protein: Optional[float] = None,
    max_calories: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    جستجوی غذاها
    """
    service = FoodService(db)
    
    search_params = FoodSearch(
        query=q,
        category_id=category_id,
        min_protein=min_protein,
        max_calories=max_calories,
        page=page,
        page_size=page_size
    )
    
    return service.search(search_params)


@router.get("/high-protein", response_model=List[FoodResponse])
def get_high_protein_foods(
    min_protein: float = Query(20, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    غذاهای با پروتئین بالا
    """
    service = FoodService(db)
    return service.get_high_protein_foods(min_protein, limit)


@router.get("/low-calorie", response_model=List[FoodResponse])
def get_low_calorie_foods(
    max_calories: float = Query(100, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    غذاهای کم‌کالری
    """
    service = FoodService(db)
    return service.get_low_calorie_foods(max_calories, limit)


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(
    food_id: int,
    db: Session = Depends(get_db),
):
    """
    دریافت اطلاعات یک غذا
    """
    service = FoodService(db)
    food = service.get_food(food_id)
    
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="غذا یافت نشد"
        )
    
    return food


@router.get("/{food_id}/calculate", response_model=CalculatedMacros)
def calculate_food_macros(
    food_id: int,
    amount: float = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """
    محاسبه ماکروها برای مقدار مشخص
    """
    service = FoodService(db)
    result = service.calculate_macros(food_id, amount)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="غذا یافت نشد"
        )
    
    return result


@router.post("", response_model=FoodResponse, status_code=status.HTTP_201_CREATED)
def create_custom_food(
    food_data: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    ایجاد غذای سفارشی
    """
    service = FoodService(db)
    return service.create_food(food_data, is_custom=True)


@router.get("/category/{category_id}", response_model=List[FoodResponse])
def get_foods_by_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    دریافت غذاهای یک دسته‌بندی
    """
    service = FoodService(db)
    return service.get_foods_by_category(category_id)
