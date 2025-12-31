"""
Calculator Routes
=================
مسیرهای محاسبات تغذیه و تمرین
"""

from typing import Optional, List
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.core.calculator import NutritionCalculator, Gender, Goal, ActivityLevel
from app.core.training_engine import TrainingEngine, ExperienceLevel
from app.core.diet_engine import DietEngine, MealType

router = APIRouter()
calculator = NutritionCalculator()
training_engine = TrainingEngine()
diet_engine = DietEngine()


# ===== Request Models =====

class BMRRequest(BaseModel):
    weight: float = Field(..., ge=30, le=300, description="وزن (کیلوگرم)")
    height: float = Field(..., ge=100, le=250, description="قد (سانتی‌متر)")
    age: int = Field(..., ge=10, le=100, description="سن")
    gender: Gender
    body_fat: Optional[float] = Field(None, ge=1, le=60, description="درصد چربی (اختیاری)")


class MacrosRequest(BMRRequest):
    activity_level: ActivityLevel
    goal: Goal


class OneRMRequest(BaseModel):
    weight: float = Field(..., gt=0, description="وزن استفاده شده")
    reps: int = Field(..., ge=1, le=30, description="تعداد تکرار")


class WaterIntakeRequest(BaseModel):
    weight: float = Field(..., ge=30, le=300)
    activity_level: str
    is_training_day: bool = False


class BodyFatRequest(BaseModel):
    weight: float = Field(..., ge=30, le=300)
    waist: float = Field(..., ge=40, le=200, description="دور کمر (cm)")
    neck: float = Field(..., ge=20, le=60, description="دور گردن (cm)")
    height: float = Field(..., ge=100, le=250)
    gender: Gender
    hip: Optional[float] = Field(None, ge=50, le=200, description="دور باسن (فقط زنان)")


# ===== Nutrition Endpoints =====

@router.post("/bmr")
def calculate_bmr(data: BMRRequest):
    """
    محاسبه BMR (متابولیسم پایه)
    
    دو روش محاسبه:
    - **Mifflin-St Jeor**: بدون درصد چربی
    - **Katch-McArdle**: با درصد چربی (دقیق‌تر)
    """
    if data.body_fat:
        bmr = calculator.calculate_bmr_katch_mcardle(data.weight, data.body_fat)
        method = "Katch-McArdle"
    else:
        bmr = calculator.calculate_bmr(data.weight, data.height, data.age, data.gender)
        method = "Mifflin-St Jeor"
    
    return {
        "bmr": round(bmr),
        "method": method,
        "unit": "kcal/day",
        "description": "کالری مورد نیاز بدن در حالت استراحت کامل"
    }


@router.post("/tdee")
def calculate_tdee(data: MacrosRequest):
    """
    محاسبه TDEE (کالری روزانه)
    """
    if data.body_fat:
        bmr = calculator.calculate_bmr_katch_mcardle(data.weight, data.body_fat)
    else:
        bmr = calculator.calculate_bmr(data.weight, data.height, data.age, data.gender)
    
    tdee = calculator.calculate_tdee(bmr, data.activity_level)
    
    return {
        "bmr": round(bmr),
        "tdee": tdee,
        "activity_level": data.activity_level.value,
        "multiplier": calculator.ACTIVITY_MULTIPLIERS[data.activity_level],
        "description": "کالری مورد نیاز روزانه با در نظر گرفتن فعالیت"
    }


@router.post("/macros")
def calculate_macros(data: MacrosRequest):
    """
    محاسبه کامل ماکروها
    
    شامل: BMR، TDEE، پروتئین، کربوهیدرات، چربی
    """
    result = calculator.get_full_calculation(
        weight=data.weight,
        height=data.height,
        age=data.age,
        gender=data.gender,
        activity_level=data.activity_level,
        goal=data.goal,
        body_fat=data.body_fat
    )
    return result


@router.post("/bmi")
def calculate_bmi(
    weight: float = Query(..., ge=30, le=300),
    height: float = Query(..., ge=100, le=250)
):
    """
    محاسبه BMI و دسته‌بندی
    """
    return calculator.calculate_bmi(weight, height)


@router.post("/ideal-weight")
def calculate_ideal_weight(
    height: float = Query(..., ge=100, le=250),
    gender: Gender = Query(...)
):
    """
    محاسبه محدوده وزن ایده‌آل
    """
    return calculator.calculate_ideal_weight(height, gender)


@router.post("/body-fat")
def estimate_body_fat(data: BodyFatRequest):
    """
    تخمین درصد چربی بدن با فرمول نیروی دریایی آمریکا
    """
    try:
        body_fat = calculator.estimate_body_fat(
            weight=data.weight,
            waist=data.waist,
            neck=data.neck,
            height=data.height,
            gender=data.gender,
            hip=data.hip
        )
        return {
            "body_fat_percentage": body_fat,
            "method": "US Navy Method",
            "note": "این یک تخمین است. برای دقت بالاتر از روش‌های حرفه‌ای استفاده کنید."
        }
    except ValueError as e:
        return {"error": str(e)}


@router.post("/water-intake")
def calculate_water_intake(data: WaterIntakeRequest):
    """
    محاسبه آب مورد نیاز روزانه
    """
    return diet_engine.calculate_water_intake(
        data.weight,
        data.activity_level,
        data.is_training_day
    )


# ===== Training Endpoints =====

@router.post("/1rm")
def calculate_one_rm(data: OneRMRequest):
    """
    تخمین 1RM (یک تکرار بیشینه)
    """
    one_rm = training_engine.calculate_1rm(data.weight, data.reps)
    
    return {
        "estimated_1rm": round(one_rm, 1),
        "input_weight": data.weight,
        "input_reps": data.reps,
        "method": "Brzycki Formula",
        "percentages": {
            "90%": round(one_rm * 0.9, 1),
            "85%": round(one_rm * 0.85, 1),
            "80%": round(one_rm * 0.8, 1),
            "75%": round(one_rm * 0.75, 1),
            "70%": round(one_rm * 0.7, 1),
        }
    }


@router.get("/training-split")
def suggest_training_split(
    experience: ExperienceLevel = Query(...),
    available_days: int = Query(4, ge=2, le=7)
):
    """
    پیشنهاد تقسیم‌بندی تمرینی
    """
    return training_engine.suggest_split(experience, available_days)


@router.get("/rep-ranges")
def get_rep_ranges():
    """
    محدوده تکرار بر اساس هدف
    """
    return training_engine.REP_RANGES_BY_GOAL


@router.post("/working-weight")
def calculate_working_weight(
    one_rm: float = Query(..., gt=0),
    target_reps: int = Query(..., ge=1, le=20),
    goal: Goal = Query(Goal.BULK)
):
    """
    محاسبه وزن کاری بر اساس 1RM
    """
    return training_engine.calculate_working_weight(one_rm, target_reps, goal)


@router.post("/progression")
def generate_progression(
    current_weight: float = Query(..., gt=0),
    current_reps: int = Query(..., ge=1, le=20),
    weeks: int = Query(4, ge=1, le=12)
):
    """
    تولید برنامه پیشرفت تدریجی
    """
    return training_engine.generate_progression(current_weight, current_reps, weeks)


# ===== Diet Endpoints =====

@router.post("/distribute-macros")
def distribute_macros(
    total_calories: int = Query(..., ge=500, le=10000),
    total_protein: int = Query(..., ge=0, le=500),
    total_carbs: int = Query(..., ge=0, le=1000),
    total_fat: int = Query(..., ge=0, le=500),
    meal_plan_type: str = Query("standard"),
    num_meals: int = Query(5, ge=3, le=8)
):
    """
    توزیع ماکروها بین وعده‌ها
    """
    return diet_engine.distribute_macros(
        total_calories,
        total_protein,
        total_carbs,
        total_fat,
        meal_plan_type,
        num_meals
    )
