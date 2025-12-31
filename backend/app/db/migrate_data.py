#!/usr/bin/env python3
"""
FLEX PRO Data Migration Script
===============================
این اسکریپت داده‌های JSON رو به دیتابیس SQLite منتقل می‌کنه

نویسنده: FLEX PRO Team
تاریخ: 2024
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.food import FoodCategory, Food
from app.models.exercise import MuscleGroup, Exercise, ExerciseType, Equipment
from app.models.supplement import SupplementCategory, Supplement


# Path to data files
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_json(filename: str) -> dict:
    """Load JSON file from data directory"""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"❌ فایل پیدا نشد: {filepath}")
        return {}
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def migrate_foods(db: Session) -> int:
    """
    مهاجرت داده‌های غذایی به دیتابیس
    """
    print("\n🍎 شروع مهاجرت داده‌های غذایی...")
    
    data = load_json("foods.json")
    if not data:
        return 0
    
    categories = data.get("categories", [])
    total_foods = 0
    
    for cat_data in categories:
        # Check if category exists
        existing_cat = db.query(FoodCategory).filter(
            FoodCategory.name == cat_data["name"]
        ).first()
        
        if existing_cat:
            category = existing_cat
            print(f"  ⏭️  دسته‌بندی '{cat_data['name']}' از قبل وجود دارد")
        else:
            # Create category
            category = FoodCategory(
                name=cat_data["name"],
                name_en=cat_data.get("name_en"),
                icon=cat_data.get("icon"),
                sort_order=cat_data.get("sort_order", 0)
            )
            db.add(category)
            db.flush()  # Get ID
            print(f"  ✅ دسته‌بندی ایجاد شد: {cat_data['name']}")
        
        # Add foods
        for food_data in cat_data.get("foods", []):
            # Check if food exists
            existing_food = db.query(Food).filter(
                Food.name == food_data["name"],
                Food.category_id == category.id
            ).first()
            
            if existing_food:
                continue  # Skip existing
            
            food = Food(
                name=food_data["name"],
                category_id=category.id,
                unit=food_data.get("unit", "گرم"),
                base_amount=food_data.get("base_amount", 100),
                calories=food_data.get("calories", 0),
                protein=food_data.get("protein", 0),
                carbs=food_data.get("carbs", 0),
                fat=food_data.get("fat", 0),
                fiber=food_data.get("fiber"),
                sugar=food_data.get("sugar"),
                sodium=food_data.get("sodium"),
                is_active=True
            )
            db.add(food)
            total_foods += 1
    
    db.commit()
    print(f"  📊 تعداد {total_foods} غذا اضافه شد")
    return total_foods


def migrate_exercises(db: Session) -> int:
    """
    مهاجرت داده‌های تمرینات به دیتابیس
    """
    print("\n🏋️ شروع مهاجرت داده‌های تمرینات...")
    
    data = load_json("exercises.json")
    if not data:
        return 0
    
    total_exercises = 0
    
    # Resistance exercises
    resistance_data = data.get("resistance_exercises", {})
    muscle_groups = resistance_data.get("muscle_groups", [])
    
    for mg_data in muscle_groups:
        # Check if muscle group exists
        existing_mg = db.query(MuscleGroup).filter(
            MuscleGroup.name == mg_data["name"]
        ).first()
        
        if existing_mg:
            muscle_group = existing_mg
            print(f"  ⏭️  گروه عضلانی '{mg_data['name']}' از قبل وجود دارد")
        else:
            # Create muscle group
            muscle_group = MuscleGroup(
                name=mg_data["name"],
                name_en=mg_data.get("name_en"),
                icon=mg_data.get("icon")
            )
            db.add(muscle_group)
            db.flush()
            print(f"  ✅ گروه عضلانی ایجاد شد: {mg_data['name']}")
        
        # Add exercises from subgroups
        for subgroup in mg_data.get("subgroups", []):
            for ex_data in subgroup.get("exercises", []):
                # Check if exercise exists
                existing_ex = db.query(Exercise).filter(
                    Exercise.name == ex_data["name"]
                ).first()
                
                if existing_ex:
                    continue
                
                # Map equipment string to enum
                equipment_map = {
                    "هالتر": Equipment.BARBELL,
                    "دمبل": Equipment.DUMBBELL,
                    "کابل": Equipment.CABLE,
                    "دستگاه": Equipment.MACHINE,
                    "وزن بدن": Equipment.BODYWEIGHT,
                    "کتل‌بل": Equipment.KETTLEBELL,
                    "کش": Equipment.RESISTANCE_BAND,
                    "اسمیت": Equipment.SMITH_MACHINE,
                    "وزنه": Equipment.BARBELL,
                    "توپ": Equipment.OTHER,
                    "چرخ شکم": Equipment.OTHER,
                    "هالتر EZ": Equipment.BARBELL,
                }
                equipment_str = ex_data.get("equipment")
                equipment = equipment_map.get(equipment_str) if equipment_str else None
                
                # Determine if compound
                is_compound = ex_data.get("type") == "compound"
                
                exercise = Exercise(
                    name=ex_data["name"],
                    name_en=ex_data.get("name_en"),
                    muscle_group_id=muscle_group.id,
                    secondary_muscles=subgroup.get("name"),
                    type=ExerciseType.RESISTANCE,
                    equipment=equipment,
                    is_compound=is_compound,
                    is_active=True
                )
                db.add(exercise)
                total_exercises += 1
    
    # Cardio exercises
    cardio_data = data.get("cardio_exercises", {})
    
    # Create or get Cardio muscle group
    cardio_group = db.query(MuscleGroup).filter(
        MuscleGroup.name == "کاردیو"
    ).first()
    
    if not cardio_group:
        cardio_group = MuscleGroup(
            name="کاردیو",
            name_en="Cardio",
            icon="🏃"
        )
        db.add(cardio_group)
        db.flush()
        print("  ✅ گروه کاردیو ایجاد شد")
    
    for cat in cardio_data.get("categories", []):
        for ex_data in cat.get("exercises", []):
            existing_ex = db.query(Exercise).filter(
                Exercise.name == ex_data["name"]
            ).first()
            
            if existing_ex:
                continue
            
            exercise = Exercise(
                name=ex_data["name"],
                name_en=ex_data.get("name_en"),
                muscle_group_id=cardio_group.id,
                secondary_muscles=cat.get("name"),
                type=ExerciseType.CARDIO,
                is_active=True
            )
            db.add(exercise)
            total_exercises += 1
    
    # Warmup & Cooldown exercises
    warmup_group = db.query(MuscleGroup).filter(
        MuscleGroup.name == "گرم کردن"
    ).first()
    
    if not warmup_group:
        warmup_group = MuscleGroup(
            name="گرم کردن",
            name_en="Warmup",
            icon="🔥"
        )
        db.add(warmup_group)
        db.flush()
        print("  ✅ گروه گرم کردن ایجاد شد")
    
    for ex_data in data.get("warmup_exercises", []):
        existing_ex = db.query(Exercise).filter(
            Exercise.name == ex_data["name"]
        ).first()
        
        if existing_ex:
            continue
        
        exercise = Exercise(
            name=ex_data["name"],
            name_en=ex_data.get("name_en"),
            muscle_group_id=warmup_group.id,
            type=ExerciseType.WARMUP,
            is_active=True
        )
        db.add(exercise)
        total_exercises += 1
    
    cooldown_group = db.query(MuscleGroup).filter(
        MuscleGroup.name == "سرد کردن"
    ).first()
    
    if not cooldown_group:
        cooldown_group = MuscleGroup(
            name="سرد کردن",
            name_en="Cooldown",
            icon="❄️"
        )
        db.add(cooldown_group)
        db.flush()
        print("  ✅ گروه سرد کردن ایجاد شد")
    
    for ex_data in data.get("cooldown_exercises", []):
        existing_ex = db.query(Exercise).filter(
            Exercise.name == ex_data["name"]
        ).first()
        
        if existing_ex:
            continue
        
        exercise = Exercise(
            name=ex_data["name"],
            name_en=ex_data.get("name_en"),
            muscle_group_id=cooldown_group.id,
            type=ExerciseType.COOLDOWN,
            is_active=True
        )
        db.add(exercise)
        total_exercises += 1
    
    # Corrective exercises
    corrective_group = db.query(MuscleGroup).filter(
        MuscleGroup.name == "اصلاحی"
    ).first()
    
    if not corrective_group:
        corrective_group = MuscleGroup(
            name="اصلاحی",
            name_en="Corrective",
            icon="🩹"
        )
        db.add(corrective_group)
        db.flush()
        print("  ✅ گروه اصلاحی ایجاد شد")
    
    corrective_data = data.get("corrective_exercises", {})
    for condition in corrective_data.get("conditions", []):
        for ex_data in condition.get("exercises", []):
            existing_ex = db.query(Exercise).filter(
                Exercise.name == ex_data["name"]
            ).first()
            
            if existing_ex:
                continue
            
            exercise = Exercise(
                name=ex_data["name"],
                name_en=ex_data.get("name_en"),
                muscle_group_id=corrective_group.id,
                secondary_muscles=condition.get("name"),
                type=ExerciseType.CORRECTIVE,
                is_active=True
            )
            db.add(exercise)
            total_exercises += 1
    
    db.commit()
    print(f"  📊 تعداد {total_exercises} تمرین اضافه شد")
    return total_exercises


def migrate_supplements(db: Session) -> int:
    """
    مهاجرت داده‌های مکمل‌ها به دیتابیس
    """
    print("\n💊 شروع مهاجرت داده‌های مکمل‌ها...")
    
    data = load_json("supplements.json")
    if not data:
        return 0
    
    categories = data.get("categories", [])
    total_supplements = 0
    
    for cat_data in categories:
        # Check if category exists
        existing_cat = db.query(SupplementCategory).filter(
            SupplementCategory.name == cat_data["name"]
        ).first()
        
        if existing_cat:
            category = existing_cat
            print(f"  ⏭️  دسته‌بندی '{cat_data['name']}' از قبل وجود دارد")
        else:
            # Create category
            category = SupplementCategory(
                name=cat_data["name"],
                name_en=cat_data.get("name_en"),
                icon=cat_data.get("icon"),
                sort_order=cat_data.get("sort_order", 0)
            )
            db.add(category)
            db.flush()
            print(f"  ✅ دسته‌بندی ایجاد شد: {cat_data['name']}")
        
        # Add supplements
        for supp_data in cat_data.get("supplements", []):
            # Check if supplement exists
            existing_supp = db.query(Supplement).filter(
                Supplement.name == supp_data["name"],
                Supplement.category_id == category.id
            ).first()
            
            if existing_supp:
                continue
            
            # Convert timing list to string
            timing = supp_data.get("timing", [])
            if isinstance(timing, list):
                timing = ", ".join(timing)
            
            supplement = Supplement(
                name=supp_data["name"],
                name_en=supp_data.get("name_en"),
                category_id=category.id,
                dose_unit=supp_data.get("type"),  # Store type as dose_unit
                suggested_time=timing,
                is_active=True
            )
            db.add(supplement)
            total_supplements += 1
    
    db.commit()
    print(f"  📊 تعداد {total_supplements} مکمل اضافه شد")
    return total_supplements


def create_tables() -> None:
    """ایجاد تمام جداول دیتابیس"""
    print("🔨 ایجاد جداول دیتابیس...")
    Base.metadata.create_all(bind=engine)
    print("✅ جداول ایجاد شدند")


def run_migration(
    foods: bool = True,
    exercises: bool = True,
    supplements: bool = True
) -> dict:
    """
    اجرای فرآیند مهاجرت
    
    Args:
        foods: آیا داده‌های غذایی مهاجرت شوند؟
        exercises: آیا داده‌های تمرینات مهاجرت شوند؟
        supplements: آیا داده‌های مکمل‌ها مهاجرت شوند؟
    
    Returns:
        dict با تعداد رکوردهای اضافه شده
    """
    print("=" * 50)
    print("🚀 FLEX PRO Data Migration")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
    # Stats
    stats = {
        "foods": 0,
        "exercises": 0,
        "supplements": 0
    }
    
    # Run migrations
    db = SessionLocal()
    try:
        if foods:
            stats["foods"] = migrate_foods(db)
        
        if exercises:
            stats["exercises"] = migrate_exercises(db)
        
        if supplements:
            stats["supplements"] = migrate_supplements(db)
        
    except Exception as e:
        print(f"\n❌ خطا در مهاجرت: {e}")
        db.rollback()
        raise
    finally:
        db.close()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 خلاصه مهاجرت:")
    print("=" * 50)
    print(f"  🍎 غذاها: {stats['foods']} رکورد")
    print(f"  🏋️ تمرینات: {stats['exercises']} رکورد")
    print(f"  💊 مکمل‌ها: {stats['supplements']} رکورد")
    print(f"  📦 مجموع: {sum(stats.values())} رکورد")
    print("=" * 50)
    print("✅ مهاجرت با موفقیت انجام شد!")
    
    return stats


def clear_data(db: Session, table: str) -> None:
    """پاک کردن داده‌های یک جدول"""
    if table == "foods":
        db.query(Food).delete()
        db.query(FoodCategory).delete()
    elif table == "exercises":
        db.query(Exercise).delete()
        db.query(MuscleGroup).delete()
    elif table == "supplements":
        db.query(Supplement).delete()
        db.query(SupplementCategory).delete()
    db.commit()


def reset_and_migrate() -> dict:
    """پاک کردن تمام داده‌ها و مهاجرت مجدد"""
    print("⚠️  پاک کردن تمام داده‌های قبلی...")
    
    db = SessionLocal()
    try:
        clear_data(db, "foods")
        clear_data(db, "exercises")
        clear_data(db, "supplements")
        print("✅ داده‌های قبلی پاک شدند")
    finally:
        db.close()
    
    return run_migration()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FLEX PRO Data Migration Tool"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="پاک کردن داده‌های قبلی و مهاجرت مجدد"
    )
    parser.add_argument(
        "--foods-only",
        action="store_true",
        help="فقط داده‌های غذایی"
    )
    parser.add_argument(
        "--exercises-only",
        action="store_true",
        help="فقط داده‌های تمرینات"
    )
    parser.add_argument(
        "--supplements-only",
        action="store_true",
        help="فقط داده‌های مکمل‌ها"
    )
    
    args = parser.parse_args()
    
    if args.reset:
        reset_and_migrate()
    elif args.foods_only:
        run_migration(foods=True, exercises=False, supplements=False)
    elif args.exercises_only:
        run_migration(foods=False, exercises=True, supplements=False)
    elif args.supplements_only:
        run_migration(foods=False, exercises=False, supplements=True)
    else:
        run_migration()
