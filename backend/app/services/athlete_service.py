"""
Athlete Service
===============
سرویس مدیریت شاگردان (ورزشکاران)
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_

from app.models.athlete import Athlete, AthleteInjury, AthleteMeasurement
from app.schemas.athlete import (
    AthleteCreate, AthleteUpdate, 
    InjuryCreate, MeasurementCreate
)
from app.core.calculator import NutritionCalculator


class AthleteService:
    """سرویس مدیریت شاگردان"""
    
    def __init__(self, db: Session):
        self.db = db
        self.calculator = NutritionCalculator()
    
    def get_by_id(self, athlete_id: int, coach_id: Optional[int] = None) -> Optional[Athlete]:
        """دریافت شاگرد با شناسه"""
        stmt = select(Athlete).options(
            joinedload(Athlete.injuries),
            joinedload(Athlete.measurements),
        ).where(Athlete.id == athlete_id)
        
        if coach_id:
            stmt = stmt.where(Athlete.coach_id == coach_id)
        
        return self.db.execute(stmt).unique().scalar_one_or_none()
    
    def get_all_by_coach(
        self, 
        coach_id: int, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = False
    ) -> List[Athlete]:
        """دریافت لیست شاگردان یک مربی"""
        stmt = select(Athlete).where(Athlete.coach_id == coach_id)
        
        if active_only:
            stmt = stmt.where(Athlete.is_active == True)
        
        stmt = stmt.order_by(Athlete.created_at.desc()).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())
    
    def create(self, coach_id: int, athlete_data: AthleteCreate) -> Athlete:
        """ایجاد شاگرد جدید"""
        data = athlete_data.model_dump(exclude={"injuries"})
        
        athlete = Athlete(
            coach_id=coach_id,
            **data
        )
        
        # افزودن آسیب‌ها
        if athlete_data.injuries:
            for injury_data in athlete_data.injuries:
                injury = AthleteInjury(**injury_data.model_dump())
                athlete.injuries.append(injury)
        
        self.db.add(athlete)
        self.db.commit()
        self.db.refresh(athlete)
        return athlete
    
    def update(
        self, 
        athlete_id: int, 
        athlete_data: AthleteUpdate,
        coach_id: Optional[int] = None
    ) -> Optional[Athlete]:
        """ویرایش شاگرد"""
        athlete = self.get_by_id(athlete_id, coach_id)
        if not athlete:
            return None
        
        update_data = athlete_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(athlete, field, value)
        
        self.db.commit()
        self.db.refresh(athlete)
        return athlete
    
    def delete(self, athlete_id: int, coach_id: Optional[int] = None) -> bool:
        """حذف شاگرد"""
        athlete = self.get_by_id(athlete_id, coach_id)
        if not athlete:
            return False
        
        self.db.delete(athlete)
        self.db.commit()
        return True
    
    def toggle_active(self, athlete_id: int, coach_id: Optional[int] = None) -> Optional[Athlete]:
        """تغییر وضعیت فعال/غیرفعال"""
        athlete = self.get_by_id(athlete_id, coach_id)
        if not athlete:
            return None
        
        athlete.is_active = not athlete.is_active
        self.db.commit()
        self.db.refresh(athlete)
        return athlete
    
    # ===== Injuries =====
    
    def add_injury(self, athlete_id: int, injury_data: InjuryCreate) -> Optional[AthleteInjury]:
        """افزودن آسیب"""
        athlete = self.db.get(Athlete, athlete_id)
        if not athlete:
            return None
        
        injury = AthleteInjury(
            athlete_id=athlete_id,
            **injury_data.model_dump()
        )
        
        self.db.add(injury)
        self.db.commit()
        self.db.refresh(injury)
        return injury
    
    def remove_injury(self, injury_id: int) -> bool:
        """حذف آسیب"""
        injury = self.db.get(AthleteInjury, injury_id)
        if not injury:
            return False
        
        self.db.delete(injury)
        self.db.commit()
        return True
    
    def update_injury(self, injury_id: int, is_healed: bool) -> Optional[AthleteInjury]:
        """بروزرسانی وضعیت آسیب"""
        injury = self.db.get(AthleteInjury, injury_id)
        if not injury:
            return None
        
        injury.is_healed = is_healed
        self.db.commit()
        self.db.refresh(injury)
        return injury
    
    # ===== Measurements =====
    
    def add_measurement(
        self, 
        athlete_id: int, 
        measurement_data: MeasurementCreate
    ) -> Optional[AthleteMeasurement]:
        """ثبت اندازه‌گیری جدید"""
        athlete = self.db.get(Athlete, athlete_id)
        if not athlete:
            return None
        
        measurement = AthleteMeasurement(
            athlete_id=athlete_id,
            **measurement_data.model_dump()
        )
        
        # بروزرسانی وزن در پروفایل اصلی
        if measurement_data.weight:
            athlete.weight = measurement_data.weight
        
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement
    
    def get_measurements(
        self, 
        athlete_id: int, 
        limit: int = 10
    ) -> List[AthleteMeasurement]:
        """دریافت تاریخچه اندازه‌گیری‌ها"""
        stmt = (
            select(AthleteMeasurement)
            .where(AthleteMeasurement.athlete_id == athlete_id)
            .order_by(AthleteMeasurement.recorded_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
    
    # ===== Calculations =====
    
    def calculate_nutrition(self, athlete_id: int) -> Optional[dict]:
        """محاسبه نیازهای تغذیه‌ای شاگرد"""
        athlete = self.get_by_id(athlete_id)
        if not athlete:
            return None
        
        if not all([athlete.weight, athlete.height, athlete.age, athlete.gender]):
            return {"error": "اطلاعات ناقص - وزن، قد، سن و جنسیت الزامی است"}
        
        # دریافت آخرین درصد چربی
        body_fat = None
        if athlete.measurements:
            latest = athlete.measurements[0]
            body_fat = latest.body_fat
        
        result = self.calculator.get_full_calculation(
            weight=athlete.weight,
            height=athlete.height,
            age=athlete.age,
            gender=athlete.gender.value if athlete.gender else "male",
            activity_level=athlete.activity_level.value if athlete.activity_level else "moderate",
            goal=athlete.goal.value if athlete.goal else "maintain",
            body_fat=body_fat
        )
        
        # اضافه کردن BMI و وزن ایده‌آل
        result["bmi"] = self.calculator.calculate_bmi(athlete.weight, athlete.height)
        result["ideal_weight"] = self.calculator.calculate_ideal_weight(
            athlete.height, 
            athlete.gender.value if athlete.gender else "male"
        )
        
        return result
    
    def count_by_coach(self, coach_id: int, active_only: bool = False) -> int:
        """تعداد شاگردان یک مربی"""
        stmt = select(Athlete).where(Athlete.coach_id == coach_id)
        if active_only:
            stmt = stmt.where(Athlete.is_active == True)
        return len(list(self.db.execute(stmt).scalars().all()))
    
    def search(
        self, 
        coach_id: int, 
        query: str,
        limit: int = 20
    ) -> List[Athlete]:
        """جستجوی شاگردان"""
        stmt = (
            select(Athlete)
            .where(
                and_(
                    Athlete.coach_id == coach_id,
                    Athlete.name.ilike(f"%{query}%")
                )
            )
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())
