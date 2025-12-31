"""
Training Engine
===============
موتور هوشمند برنامه‌ریزی تمرینی
"""

from typing import List, Dict, Optional, Set
from enum import Enum


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


class Goal(str, Enum):
    BULK = "bulk"
    CUT = "cut"
    STRENGTH = "strength"
    ENDURANCE = "endurance"


class SplitType(str, Enum):
    FULL_BODY = "full_body"           # تمام بدن
    UPPER_LOWER = "upper_lower"       # بالاتنه/پایین‌تنه
    PPL = "push_pull_legs"            # هل/کشش/پا
    BRO_SPLIT = "bro_split"           # هر روز یک عضله
    ARNOLD = "arnold"                 # آرنولد (۶ روزه)


class TrainingEngine:
    """
    موتور برنامه‌ریزی تمرین
    ========================
    پیشنهاد و بهینه‌سازی برنامه تمرینی بر اساس سطح و هدف
    """
    
    # تقسیم‌بندی پیشنهادی بر اساس سطح
    SPLIT_RECOMMENDATIONS = {
        ExperienceLevel.BEGINNER: {
            "split": SplitType.FULL_BODY,
            "days_per_week": 3,
            "sets_per_muscle": 6,    # ست در هفته برای هر عضله
            "rep_range": "8-12",
            "rest_seconds": 90,
        },
        ExperienceLevel.INTERMEDIATE: {
            "split": SplitType.UPPER_LOWER,
            "days_per_week": 4,
            "sets_per_muscle": 12,
            "rep_range": "6-12",
            "rest_seconds": 75,
        },
        ExperienceLevel.ADVANCED: {
            "split": SplitType.PPL,
            "days_per_week": 6,
            "sets_per_muscle": 16,
            "rep_range": "4-15",
            "rest_seconds": 60,
        },
        ExperienceLevel.ELITE: {
            "split": SplitType.ARNOLD,
            "days_per_week": 6,
            "sets_per_muscle": 20,
            "rep_range": "1-20",
            "rest_seconds": 45,
        },
    }
    
    # ترتیب عضلات در هر تقسیم‌بندی
    SPLIT_TEMPLATES = {
        SplitType.FULL_BODY: [
            ["سینه", "پشت", "شانه", "پا", "جلوبازو", "پشت‌بازو"],
            ["پا", "سینه", "پشت", "شانه", "پشت‌بازو", "جلوبازو"],
            ["پشت", "سینه", "پا", "شانه", "جلوبازو", "پشت‌بازو"],
        ],
        SplitType.UPPER_LOWER: [
            ["سینه", "پشت", "شانه", "جلوبازو", "پشت‌بازو"],  # بالاتنه
            ["چهارسر", "همسترینگ", "سرینی", "ساق"],          # پایین‌تنه
            ["سینه", "پشت", "شانه", "جلوبازو", "پشت‌بازو"],  # بالاتنه
            ["چهارسر", "همسترینگ", "سرینی", "ساق"],          # پایین‌تنه
        ],
        SplitType.PPL: [
            ["سینه", "شانه", "پشت‌بازو"],     # Push
            ["پشت", "جلوبازو", "ساعد"],       # Pull
            ["چهارسر", "همسترینگ", "ساق"],    # Legs
            ["سینه", "شانه", "پشت‌بازو"],     # Push
            ["پشت", "جلوبازو", "ساعد"],       # Pull
            ["چهارسر", "همسترینگ", "ساق"],    # Legs
        ],
    }
    
    # محدوده تکرار بر اساس هدف
    REP_RANGES_BY_GOAL = {
        Goal.STRENGTH: {"min": 1, "max": 5, "description": "قدرت خالص"},
        Goal.BULK: {"min": 6, "max": 12, "description": "هایپرتروفی"},
        Goal.CUT: {"min": 8, "max": 15, "description": "حفظ عضله + سوزاندن چربی"},
        Goal.ENDURANCE: {"min": 15, "max": 25, "description": "استقامت عضلانی"},
    }
    
    # حرکات ممنوعه برای آسیب‌های خاص
    INJURY_EXERCISE_RESTRICTIONS = {
        "کمر": ["ددلیفت", "اسکات با وزنه سنگین", "گودمورنینگ", "بارفیکس"],
        "زانو": ["اسکات عمیق", "لانج", "لگ پرس با زاویه بسته", "پرش"],
        "شانه": ["پرس سرشانه پشت گردن", "آپرایت رو", "دیپ عمیق"],
        "آرنج": ["پشت‌بازو پرسی", "کرل هالتر سنگین"],
        "مچ دست": ["پرس سینه هالتر", "شنا روی مشت"],
    }
    
    def suggest_split(
        self,
        experience_level: ExperienceLevel,
        available_days: int = 4
    ) -> Dict:
        """
        پیشنهاد تقسیم‌بندی تمرینی
        
        Args:
            experience_level: سطح تجربه
            available_days: تعداد روزهای در دسترس
            
        Returns:
            تقسیم‌بندی پیشنهادی
        """
        base_recommendation = self.SPLIT_RECOMMENDATIONS[experience_level].copy()
        
        # تنظیم بر اساس روزهای در دسترس
        if available_days <= 2:
            base_recommendation["split"] = SplitType.FULL_BODY
            base_recommendation["days_per_week"] = 2
        elif available_days == 3:
            if experience_level in [ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE]:
                base_recommendation["split"] = SplitType.FULL_BODY
            else:
                base_recommendation["split"] = SplitType.PPL
            base_recommendation["days_per_week"] = 3
        elif available_days == 4:
            base_recommendation["split"] = SplitType.UPPER_LOWER
            base_recommendation["days_per_week"] = 4
        elif available_days >= 5:
            if experience_level in [ExperienceLevel.ADVANCED, ExperienceLevel.ELITE]:
                base_recommendation["split"] = SplitType.PPL
                base_recommendation["days_per_week"] = min(available_days, 6)
        
        return base_recommendation
    
    def get_rep_range(self, goal: Goal) -> Dict:
        """
        دریافت محدوده تکرار بر اساس هدف
        """
        return self.REP_RANGES_BY_GOAL.get(goal, self.REP_RANGES_BY_GOAL[Goal.BULK])
    
    def get_restricted_exercises(self, injuries: List[str]) -> Set[str]:
        """
        لیست حرکات ممنوعه بر اساس آسیب‌های ورزشکار
        
        Args:
            injuries: لیست آسیب‌ها
            
        Returns:
            مجموعه حرکات ممنوعه
        """
        restricted = set()
        for injury in injuries:
            injury_lower = injury.lower()
            for body_part, exercises in self.INJURY_EXERCISE_RESTRICTIONS.items():
                if body_part in injury_lower:
                    restricted.update(exercises)
        return restricted
    
    def calculate_volume(
        self,
        experience_level: ExperienceLevel,
        muscle_group: str,
        goal: Goal
    ) -> Dict:
        """
        محاسبه حجم تمرینی مناسب
        
        Args:
            experience_level: سطح تجربه
            muscle_group: گروه عضلانی
            goal: هدف
            
        Returns:
            تعداد ست و تکرار پیشنهادی
        """
        base = self.SPLIT_RECOMMENDATIONS[experience_level]
        rep_range = self.REP_RANGES_BY_GOAL[goal]
        
        # تنظیم حجم برای گروه‌های عضلانی مختلف
        volume_multipliers = {
            "پا": 1.2,      # عضلات بزرگ نیاز به حجم بیشتر
            "پشت": 1.1,
            "سینه": 1.0,
            "شانه": 0.8,
            "بازو": 0.7,    # عضلات کوچک نیاز به حجم کمتر
        }
        
        multiplier = 1.0
        for key, val in volume_multipliers.items():
            if key in muscle_group:
                multiplier = val
                break
        
        sets_per_week = round(base["sets_per_muscle"] * multiplier)
        
        return {
            "sets_per_week": sets_per_week,
            "sets_per_session": round(sets_per_week / (base["days_per_week"] / 2)),
            "rep_range": f"{rep_range['min']}-{rep_range['max']}",
            "rest_seconds": base["rest_seconds"],
        }
    
    def calculate_1rm(self, weight: float, reps: int) -> float:
        """
        تخمین 1RM با فرمول Brzycki
        
        Args:
            weight: وزن استفاده شده
            reps: تعداد تکرار انجام شده
            
        Returns:
            تخمین یک تکرار بیشینه
        """
        if reps == 1:
            return weight
        if reps > 12:
            # فرمول برای تکرار بالا دقیق نیست
            return weight * (1 + 0.025 * reps)
        
        # فرمول Brzycki
        return weight * (36 / (37 - reps))
    
    def calculate_working_weight(
        self,
        one_rm: float,
        target_reps: int,
        goal: Goal
    ) -> Dict[str, float]:
        """
        محاسبه وزن کاری بر اساس 1RM
        
        Args:
            one_rm: یک تکرار بیشینه
            target_reps: تکرار هدف
            goal: هدف تمرینی
            
        Returns:
            وزن پیشنهادی
        """
        # درصد 1RM بر اساس تکرار
        percentage_map = {
            1: 100, 2: 95, 3: 93, 4: 90, 5: 87,
            6: 85, 7: 83, 8: 80, 9: 77, 10: 75,
            11: 73, 12: 70, 15: 65, 20: 60
        }
        
        percentage = percentage_map.get(target_reps, 70) / 100
        working_weight = one_rm * percentage
        
        return {
            "weight": round(working_weight, 1),
            "percentage_1rm": round(percentage * 100),
            "target_reps": target_reps,
        }
    
    def generate_progression(
        self,
        current_weight: float,
        current_reps: int,
        weeks: int = 4
    ) -> List[Dict]:
        """
        تولید برنامه پیشرفت تدریجی
        
        Args:
            current_weight: وزن فعلی
            current_reps: تکرار فعلی
            weeks: تعداد هفته
            
        Returns:
            برنامه پیشرفت هفتگی
        """
        progression = []
        weight = current_weight
        reps = current_reps
        
        for week in range(1, weeks + 1):
            if week % 2 == 1:
                # هفته فرد: افزایش تکرار
                reps = min(reps + 1, 12)
            else:
                # هفته زوج: افزایش وزن، کاهش تکرار
                weight = round(weight * 1.025, 1)  # 2.5% افزایش
                reps = max(reps - 2, 6)
            
            progression.append({
                "week": week,
                "weight": weight,
                "reps": reps,
                "estimated_1rm": round(self.calculate_1rm(weight, reps), 1)
            })
        
        return progression


# نمونه سینگلتون
training_engine = TrainingEngine()
