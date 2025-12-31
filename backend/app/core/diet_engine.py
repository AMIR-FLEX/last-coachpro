"""
Diet Engine
===========
موتور هوشمند برنامه‌ریزی تغذیه
"""

from typing import List, Dict, Optional
from enum import Enum


class MealType(str, Enum):
    BREAKFAST = "صبحانه"
    SNACK_1 = "میان وعده ۱"
    LUNCH = "ناهار"
    SNACK_2 = "میان وعده ۲"
    DINNER = "شام"
    SNACK_3 = "میان وعده ۳"
    PRE_WORKOUT = "قبل تمرین"
    POST_WORKOUT = "بعد تمرین"


class Goal(str, Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTAIN = "maintain"


class DietEngine:
    """
    موتور برنامه‌ریزی تغذیه
    ========================
    تقسیم ماکروها بین وعده‌ها و پیشنهاد هوشمند
    """
    
    # توزیع پیشنهادی کالری بین وعده‌ها
    MEAL_DISTRIBUTION = {
        "standard": {
            MealType.BREAKFAST: 0.25,      # 25%
            MealType.SNACK_1: 0.10,        # 10%
            MealType.LUNCH: 0.30,          # 30%
            MealType.SNACK_2: 0.10,        # 10%
            MealType.DINNER: 0.25,         # 25%
        },
        "pre_post_workout": {
            MealType.BREAKFAST: 0.20,
            MealType.PRE_WORKOUT: 0.15,
            MealType.POST_WORKOUT: 0.20,
            MealType.LUNCH: 0.25,
            MealType.DINNER: 0.20,
        },
        "intermittent_fasting": {
            MealType.LUNCH: 0.35,
            MealType.SNACK_2: 0.15,
            MealType.DINNER: 0.35,
            MealType.SNACK_3: 0.15,
        },
    }
    
    # پروتئین هر وعده (بر اساس جذب بهینه)
    PROTEIN_PER_MEAL_LIMITS = {
        "min": 20,   # حداقل پروتئین برای تحریک MPS
        "optimal": 40,  # مقدار بهینه
        "max": 50,   # حداکثر جذب در یک وعده
    }
    
    # منابع غذایی پیشنهادی بر اساس زمان
    FOOD_TIMING_SUGGESTIONS = {
        MealType.BREAKFAST: {
            "protein_sources": ["تخم مرغ", "پنیر", "ماست یونانی"],
            "carb_sources": ["جو دوسر", "نان سبوس‌دار", "میوه"],
            "tips": "صبحانه پروتئینی برای شروع متابولیسم",
        },
        MealType.PRE_WORKOUT: {
            "protein_sources": ["وی پروتئین", "سینه مرغ"],
            "carb_sources": ["برنج", "موز", "عسل"],
            "tips": "۱-۲ ساعت قبل تمرین، کربوهیدرات با GI متوسط",
        },
        MealType.POST_WORKOUT: {
            "protein_sources": ["وی پروتئین ایزوله", "سینه مرغ"],
            "carb_sources": ["برنج سفید", "سیب‌زمینی", "موز"],
            "tips": "فوری بعد تمرین، پروتئین سریع + کربوهیدرات با GI بالا",
        },
        MealType.DINNER: {
            "protein_sources": ["ماهی", "گوشت قرمز", "مرغ"],
            "carb_sources": ["سبزیجات", "سالاد"],
            "tips": "شام سبک با پروتئین آهسته‌رهش (کازئین)",
        },
    }
    
    def distribute_macros(
        self,
        total_calories: int,
        total_protein: int,
        total_carbs: int,
        total_fat: int,
        meal_plan_type: str = "standard",
        num_meals: int = 5
    ) -> List[Dict]:
        """
        توزیع ماکروها بین وعده‌ها
        
        Args:
            total_calories: کل کالری روزانه
            total_protein: کل پروتئین (گرم)
            total_carbs: کل کربوهیدرات (گرم)
            total_fat: کل چربی (گرم)
            meal_plan_type: نوع برنامه غذایی
            num_meals: تعداد وعده‌ها
            
        Returns:
            لیست وعده‌ها با ماکروها
        """
        distribution = self.MEAL_DISTRIBUTION.get(
            meal_plan_type, 
            self.MEAL_DISTRIBUTION["standard"]
        )
        
        meals = []
        for meal_type, ratio in distribution.items():
            meal = {
                "meal": meal_type.value,
                "calories": round(total_calories * ratio),
                "protein": round(total_protein * ratio),
                "carbs": round(total_carbs * ratio),
                "fat": round(total_fat * ratio),
            }
            
            # اطمینان از پروتئین کافی در هر وعده
            if meal["protein"] < self.PROTEIN_PER_MEAL_LIMITS["min"]:
                meal["protein"] = self.PROTEIN_PER_MEAL_LIMITS["min"]
            elif meal["protein"] > self.PROTEIN_PER_MEAL_LIMITS["max"]:
                meal["protein"] = self.PROTEIN_PER_MEAL_LIMITS["max"]
            
            meals.append(meal)
        
        return meals
    
    def calculate_meal_macros(
        self,
        foods: List[Dict]
    ) -> Dict:
        """
        محاسبه مجموع ماکروهای یک وعده
        
        Args:
            foods: لیست غذاها با مقدار و ماکرو
            
        Returns:
            مجموع ماکروها
        """
        totals = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
        }
        
        for food in foods:
            amount_ratio = food.get("amount", 100) / food.get("base_amount", 100)
            totals["calories"] += food.get("calories", 0) * amount_ratio
            totals["protein"] += food.get("protein", 0) * amount_ratio
            totals["carbs"] += food.get("carbs", 0) * amount_ratio
            totals["fat"] += food.get("fat", 0) * amount_ratio
            totals["fiber"] += food.get("fiber", 0) * amount_ratio
        
        return {k: round(v, 1) for k, v in totals.items()}
    
    def suggest_foods_for_meal(
        self,
        meal_type: MealType,
        target_protein: int,
        target_carbs: int,
        target_fat: int,
        allergies: Optional[List[str]] = None
    ) -> Dict:
        """
        پیشنهاد غذا برای یک وعده
        
        Args:
            meal_type: نوع وعده
            target_protein: پروتئین هدف
            target_carbs: کربوهیدرات هدف
            target_fat: چربی هدف
            allergies: حساسیت‌های غذایی
            
        Returns:
            پیشنهادات غذایی
        """
        suggestions = self.FOOD_TIMING_SUGGESTIONS.get(
            meal_type,
            {
                "protein_sources": ["سینه مرغ", "ماهی", "تخم مرغ"],
                "carb_sources": ["برنج", "نان", "سیب‌زمینی"],
                "tips": "",
            }
        )
        
        # فیلتر کردن حساسیت‌ها
        if allergies:
            allergies_lower = [a.lower() for a in allergies]
            suggestions["protein_sources"] = [
                f for f in suggestions["protein_sources"]
                if not any(a in f.lower() for a in allergies_lower)
            ]
            suggestions["carb_sources"] = [
                f for f in suggestions["carb_sources"]
                if not any(a in f.lower() for a in allergies_lower)
            ]
        
        return {
            "meal": meal_type.value,
            "targets": {
                "protein": target_protein,
                "carbs": target_carbs,
                "fat": target_fat,
            },
            "suggestions": suggestions,
        }
    
    def analyze_diet_balance(
        self,
        daily_foods: List[Dict]
    ) -> Dict:
        """
        تحلیل تعادل رژیم غذایی
        
        Args:
            daily_foods: لیست غذاهای روزانه
            
        Returns:
            تحلیل و پیشنهادات
        """
        totals = self.calculate_meal_macros(daily_foods)
        
        analysis = {
            "totals": totals,
            "issues": [],
            "suggestions": [],
        }
        
        # بررسی نسبت ماکروها
        if totals["calories"] > 0:
            protein_ratio = (totals["protein"] * 4) / totals["calories"]
            carbs_ratio = (totals["carbs"] * 4) / totals["calories"]
            fat_ratio = (totals["fat"] * 9) / totals["calories"]
            
            analysis["ratios"] = {
                "protein": round(protein_ratio * 100),
                "carbs": round(carbs_ratio * 100),
                "fat": round(fat_ratio * 100),
            }
            
            # بررسی مشکلات
            if protein_ratio < 0.20:
                analysis["issues"].append("پروتئین کم - کمتر از ۲۰٪ کالری")
                analysis["suggestions"].append("منابع پروتئینی بیشتر اضافه کنید")
            
            if fat_ratio > 0.40:
                analysis["issues"].append("چربی زیاد - بیش از ۴۰٪ کالری")
                analysis["suggestions"].append("از روغن‌ها و غذاهای چرب کم کنید")
            
            if totals["fiber"] < 25:
                analysis["issues"].append("فیبر کم - کمتر از ۲۵ گرم")
                analysis["suggestions"].append("سبزیجات و غلات کامل بیشتر مصرف کنید")
        
        return analysis
    
    def calculate_water_intake(
        self,
        weight: float,
        activity_level: str,
        is_training_day: bool = False
    ) -> Dict:
        """
        محاسبه آب مورد نیاز روزانه
        
        Args:
            weight: وزن (کیلوگرم)
            activity_level: سطح فعالیت
            is_training_day: آیا روز تمرین است
            
        Returns:
            مقدار آب پیشنهادی
        """
        # فرمول پایه: 30-40 ml به ازای هر کیلو وزن
        base_ml = weight * 35
        
        # افزایش برای فعالیت
        activity_multipliers = {
            "sedentary": 1.0,
            "light": 1.1,
            "moderate": 1.2,
            "active": 1.3,
            "very_active": 1.4,
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.2)
        daily_ml = base_ml * multiplier
        
        # افزایش برای روز تمرین
        if is_training_day:
            daily_ml += 500  # نیم لیتر اضافه
        
        return {
            "daily_ml": round(daily_ml),
            "daily_liters": round(daily_ml / 1000, 1),
            "glasses": round(daily_ml / 250),  # لیوان 250ml
            "tips": "در طول روز و نه یکجا بنوشید. ادرار باید رنگ روشن داشته باشد.",
        }


# نمونه سینگلتون
diet_engine = DietEngine()
