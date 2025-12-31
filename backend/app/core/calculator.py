"""
Nutrition Calculator
====================
موتور محاسبات تغذیه‌ای هوشمند
"""

from typing import Optional, Dict, Literal
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Goal(str, Enum):
    BULK = "bulk"           # افزایش حجم
    CUT = "cut"             # کاهش چربی
    MAINTAIN = "maintain"   # نگهداری
    RECOMP = "recomp"       # بازترکیب بدنی


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"         # کارمند پشت میزی
    LIGHT = "light"                 # فعالیت سبک
    MODERATE = "moderate"           # فعالیت متوسط
    ACTIVE = "active"               # فعالیت زیاد
    VERY_ACTIVE = "very_active"     # خیلی فعال


class NutritionCalculator:
    """
    ماشین حساب تغذیه
    =================
    محاسبه BMR، TDEE و ماکروها بر اساس اطلاعات فردی و هدف
    """
    
    # ضرایب فعالیت برای محاسبه TDEE
    ACTIVITY_MULTIPLIERS = {
        ActivityLevel.SEDENTARY: 1.2,      # بدون فعالیت
        ActivityLevel.LIGHT: 1.375,        # ۱-۳ روز ورزش در هفته
        ActivityLevel.MODERATE: 1.55,      # ۳-۵ روز ورزش در هفته
        ActivityLevel.ACTIVE: 1.725,       # ۶-۷ روز ورزش در هفته
        ActivityLevel.VERY_ACTIVE: 1.9,    # ورزشکار حرفه‌ای / کار فیزیکی سنگین
    }
    
    # تنظیمات ماکرو بر اساس هدف
    MACRO_PRESETS = {
        Goal.BULK: {
            "calorie_adjustment": 300,      # +300 کالری
            "protein_per_kg": 2.0,          # گرم پروتئین به ازای هر کیلو وزن
            "fat_percentage": 0.25,         # 25% کالری از چربی
            # باقی از کربوهیدرات
        },
        Goal.CUT: {
            "calorie_adjustment": -400,     # -400 کالری
            "protein_per_kg": 2.4,          # پروتئین بالاتر در کات
            "fat_percentage": 0.25,
        },
        Goal.MAINTAIN: {
            "calorie_adjustment": 0,
            "protein_per_kg": 1.8,
            "fat_percentage": 0.30,
        },
        Goal.RECOMP: {
            "calorie_adjustment": -100,     # کسری کوچک
            "protein_per_kg": 2.2,          # پروتئین بالا
            "fat_percentage": 0.25,
        },
    }
    
    @staticmethod
    def calculate_bmr(
        weight: float,
        height: float,
        age: int,
        gender: Gender
    ) -> float:
        """
        محاسبه BMR با فرمول Mifflin-St Jeor
        دقیق‌ترین فرمول برای افراد عادی
        
        Args:
            weight: وزن (کیلوگرم)
            height: قد (سانتی‌متر)
            age: سن (سال)
            gender: جنسیت
            
        Returns:
            BMR (کالری در روز)
        """
        # فرمول: (10 × weight) + (6.25 × height) − (5 × age) + s
        # s = +5 برای مرد، -161 برای زن
        
        base = (10 * weight) + (6.25 * height) - (5 * age)
        
        if gender == Gender.MALE:
            return base + 5
        else:
            return base - 161
    
    @staticmethod
    def calculate_bmr_katch_mcardle(
        weight: float,
        body_fat_percentage: float
    ) -> float:
        """
        محاسبه BMR با فرمول Katch-McArdle
        دقیق‌تر برای کسانی که درصد چربی‌شان مشخص است
        
        Args:
            weight: وزن (کیلوگرم)
            body_fat_percentage: درصد چربی بدن
            
        Returns:
            BMR (کالری در روز)
        """
        # محاسبه توده عضلانی بدون چربی (LBM)
        lean_body_mass = weight * (1 - (body_fat_percentage / 100))
        
        # فرمول: 370 + (21.6 × LBM)
        return 370 + (21.6 * lean_body_mass)
    
    def calculate_tdee(
        self,
        bmr: float,
        activity_level: ActivityLevel
    ) -> float:
        """
        محاسبه TDEE (کالری مورد نیاز روزانه)
        
        Args:
            bmr: متابولیسم پایه
            activity_level: سطح فعالیت
            
        Returns:
            TDEE (کالری در روز)
        """
        multiplier = self.ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
        return round(bmr * multiplier)
    
    def calculate_macros(
        self,
        weight: float,
        tdee: float,
        goal: Goal
    ) -> Dict[str, int]:
        """
        محاسبه ماکروها بر اساس TDEE و هدف
        
        Args:
            weight: وزن (کیلوگرم)
            tdee: کالری روزانه
            goal: هدف (بالک، کات، نگهداری)
            
        Returns:
            دیکشنری شامل کالری و ماکروها
        """
        preset = self.MACRO_PRESETS.get(goal, self.MACRO_PRESETS[Goal.MAINTAIN])
        
        # کالری هدف
        target_calories = tdee + preset["calorie_adjustment"]
        
        # پروتئین (بر اساس وزن بدن)
        protein_grams = round(weight * preset["protein_per_kg"])
        protein_calories = protein_grams * 4
        
        # چربی (درصدی از کالری)
        fat_calories = target_calories * preset["fat_percentage"]
        fat_grams = round(fat_calories / 9)
        
        # کربوهیدرات (باقیمانده)
        remaining_calories = target_calories - protein_calories - fat_calories
        carbs_grams = round(remaining_calories / 4)
        
        return {
            "calories": round(target_calories),
            "protein": protein_grams,
            "carbs": max(carbs_grams, 50),  # حداقل 50 گرم کربوهیدرات
            "fat": fat_grams,
        }
    
    def get_full_calculation(
        self,
        weight: float,
        height: float,
        age: int,
        gender: Gender,
        activity_level: ActivityLevel,
        goal: Goal,
        body_fat: Optional[float] = None
    ) -> Dict[str, any]:
        """
        محاسبه کامل BMR، TDEE و ماکروها
        
        Returns:
            دیکشنری کامل با تمام مقادیر
        """
        # محاسبه BMR
        if body_fat:
            bmr = self.calculate_bmr_katch_mcardle(weight, body_fat)
            bmr_method = "Katch-McArdle"
        else:
            bmr = self.calculate_bmr(weight, height, age, gender)
            bmr_method = "Mifflin-St Jeor"
        
        # محاسبه TDEE
        tdee = self.calculate_tdee(bmr, activity_level)
        
        # محاسبه ماکروها
        macros = self.calculate_macros(weight, tdee, goal)
        
        return {
            "bmr": round(bmr),
            "bmr_method": bmr_method,
            "tdee": tdee,
            "activity_multiplier": self.ACTIVITY_MULTIPLIERS[activity_level],
            "goal": goal.value,
            "macros": macros,
            "macro_ratios": {
                "protein_percentage": round((macros["protein"] * 4 / macros["calories"]) * 100),
                "carbs_percentage": round((macros["carbs"] * 4 / macros["calories"]) * 100),
                "fat_percentage": round((macros["fat"] * 9 / macros["calories"]) * 100),
            }
        }
    
    @staticmethod
    def calculate_ideal_weight(
        height: float,
        gender: Gender
    ) -> Dict[str, float]:
        """
        محاسبه محدوده وزن ایده‌آل
        
        Args:
            height: قد (سانتی‌متر)
            gender: جنسیت
            
        Returns:
            محدوده وزن ایده‌آل
        """
        # فرمول Devine
        height_inches = height / 2.54
        
        if gender == Gender.MALE:
            ideal = 50 + 2.3 * (height_inches - 60)
        else:
            ideal = 45.5 + 2.3 * (height_inches - 60)
        
        return {
            "min": round(ideal * 0.9, 1),
            "ideal": round(ideal, 1),
            "max": round(ideal * 1.1, 1),
        }
    
    @staticmethod
    def calculate_bmi(weight: float, height: float) -> Dict[str, any]:
        """
        محاسبه BMI و دسته‌بندی
        
        Args:
            weight: وزن (کیلوگرم)
            height: قد (سانتی‌متر)
            
        Returns:
            BMI و دسته‌بندی
        """
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        if bmi < 18.5:
            category = "کمبود وزن"
            category_en = "Underweight"
        elif bmi < 25:
            category = "نرمال"
            category_en = "Normal"
        elif bmi < 30:
            category = "اضافه وزن"
            category_en = "Overweight"
        else:
            category = "چاق"
            category_en = "Obese"
        
        return {
            "bmi": round(bmi, 1),
            "category": category,
            "category_en": category_en,
        }
    
    @staticmethod
    def estimate_body_fat(
        weight: float,
        waist: float,
        neck: float,
        height: float,
        gender: Gender,
        hip: Optional[float] = None
    ) -> float:
        """
        تخمین درصد چربی بدن با فرمول نیروی دریایی آمریکا
        
        Args:
            weight: وزن (kg)
            waist: دور کمر (cm)
            neck: دور گردن (cm)
            height: قد (cm)
            gender: جنسیت
            hip: دور باسن (cm) - فقط برای زنان
            
        Returns:
            درصد تخمینی چربی بدن
        """
        import math
        
        if gender == Gender.MALE:
            # فرمول مردان: 86.010 × log10(waist − neck) − 70.041 × log10(height) + 36.76
            body_fat = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
        else:
            if hip is None:
                raise ValueError("برای زنان، دور باسن الزامی است")
            # فرمول زنان: 163.205 × log10(waist + hip − neck) − 97.684 × log10(height) − 78.387
            body_fat = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387
        
        return round(max(body_fat, 3), 1)  # حداقل 3%


# نمونه سینگلتون برای استفاده آسان
nutrition_calculator = NutritionCalculator()
