"""
Database Initialization
=======================
راه‌اندازی و پر کردن داده‌های اولیه دیتابیس
"""

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.food import FoodCategory, Food
from app.models.exercise import MuscleGroup, Exercise, ExerciseType
from app.models.supplement import SupplementCategory, Supplement
from app.core.security import get_password_hash


def create_tables() -> None:
    """ایجاد جداول دیتابیس"""
    Base.metadata.create_all(bind=engine)
    print("✅ جداول دیتابیس ایجاد شد")


def create_default_user(db: Session) -> None:
    """ایجاد کاربر پیش‌فرض (Idempotent)"""
    existing = db.query(User).filter(User.email == "admin@flexpro.com").first()
    if existing:
        print("ℹ️  کاربر پیش‌فرض از قبل موجود است: admin@flexpro.com")
        return
    
    admin = User(
        email="admin@flexpro.com",
        hashed_password=get_password_hash("admin123"),
        full_name="مدیر سیستم",
        is_superuser=True,
        theme="dark",
        language="fa"
    )
    db.add(admin)
    db.commit()
    print("✅ کاربر پیش‌فرض ایجاد شد: admin@flexpro.com / admin123")


def create_food_categories(db: Session) -> None:
    """ایجاد دسته‌بندی‌های غذا (Idempotent)"""
    # بررسی وجود دسته‌بندی‌های ضروری
    protein_cat = db.query(FoodCategory).filter(FoodCategory.name == "منابع پروتئین").first()
    carb_cat = db.query(FoodCategory).filter(FoodCategory.name == "منابع کربوهیدرات").first()
    
    if protein_cat and carb_cat:
        print("ℹ️  دسته‌بندی‌های غذا از قبل موجود هستند")
        return
    
    categories = [
        {"name": "منابع پروتئین", "name_en": "Protein Sources", "icon": "🥩", "sort_order": 1},
        {"name": "منابع کربوهیدرات", "name_en": "Carbohydrate Sources", "icon": "🍚", "sort_order": 2},
        {"name": "چربی‌های سالم", "name_en": "Healthy Fats", "icon": "🥑", "sort_order": 3},
        {"name": "سبزیجات", "name_en": "Vegetables", "icon": "🥗", "sort_order": 4},
        {"name": "میوه‌ها", "name_en": "Fruits", "icon": "🍎", "sort_order": 5},
        {"name": "لبنیات", "name_en": "Dairy", "icon": "🥛", "sort_order": 6},
        {"name": "نوشیدنی‌ها", "name_en": "Beverages", "icon": "🥤", "sort_order": 7},
        {"name": "تنقلات سالم", "name_en": "Healthy Snacks", "icon": "🥜", "sort_order": 8},
    ]
    
    for cat_data in categories:
        category = FoodCategory(**cat_data)
        db.add(category)
    
    db.commit()
    print("✅ دسته‌بندی‌های غذا ایجاد شد")


def create_sample_foods(db: Session) -> None:
    """ایجاد نمونه غذاها (Idempotent)"""
    # بررسی وجود حداقل یک غذا
    existing = db.query(Food).first()
    if existing:
        print("ℹ️  نمونه غذاها از قبل موجود هستند")
        return
    
    # دریافت دسته‌بندی پروتئین
    protein_cat = db.query(FoodCategory).filter(FoodCategory.name == "منابع پروتئین").first()
    carb_cat = db.query(FoodCategory).filter(FoodCategory.name == "منابع کربوهیدرات").first()
    
    if not protein_cat or not carb_cat:
        return
    
    # غذاهای پروتئینی
    protein_foods = [
        {"name": "سینه مرغ (پخته)", "unit": "گرم", "base_amount": 100, "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        {"name": "تخم مرغ کامل", "unit": "عدد", "base_amount": 1, "calories": 72, "protein": 6.3, "carbs": 0.4, "fat": 5},
        {"name": "ماهی سالمون (پخته)", "unit": "گرم", "base_amount": 100, "calories": 206, "protein": 22, "carbs": 0, "fat": 12},
        {"name": "گوشت قرمز کم‌چرب", "unit": "گرم", "base_amount": 100, "calories": 210, "protein": 28, "carbs": 0, "fat": 10},
        {"name": "ماست یونانی", "unit": "گرم", "base_amount": 100, "calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
    ]
    
    for food_data in protein_foods:
        food = Food(category_id=protein_cat.id, **food_data)
        db.add(food)
    
    # غذاهای کربوهیدراتی
    carb_foods = [
        {"name": "برنج سفید (پخته)", "unit": "گرم", "base_amount": 100, "calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
        {"name": "جو دوسر", "unit": "گرم", "base_amount": 100, "calories": 389, "protein": 16.9, "carbs": 66, "fat": 6.9},
        {"name": "سیب‌زمینی (پخته)", "unit": "گرم", "base_amount": 100, "calories": 77, "protein": 2, "carbs": 17, "fat": 0.1},
        {"name": "نان سبوس‌دار", "unit": "گرم", "base_amount": 100, "calories": 247, "protein": 13, "carbs": 41, "fat": 3.4},
        {"name": "موز", "unit": "عدد", "base_amount": 1, "calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4},
    ]
    
    for food_data in carb_foods:
        food = Food(category_id=carb_cat.id, **food_data)
        db.add(food)
    
    db.commit()
    print("✅ نمونه غذاها ایجاد شد")


def create_muscle_groups(db: Session) -> None:
    """ایجاد گروه‌های عضلانی (Idempotent)"""
    # بررسی وجود حداقل یک گروه عضلانی
    chest = db.query(MuscleGroup).filter(MuscleGroup.name == "سینه").first()
    back = db.query(MuscleGroup).filter(MuscleGroup.name == "پشت").first()
    
    if chest and back:
        print("ℹ️  گروه‌های عضلانی از قبل موجود هستند")
        return
    
    groups = [
        {"name": "سینه", "name_en": "Chest", "icon": "💪", "body_region": "upper", "sort_order": 1},
        {"name": "پشت", "name_en": "Back", "icon": "🔙", "body_region": "upper", "sort_order": 2},
        {"name": "شانه", "name_en": "Shoulders", "icon": "🦾", "body_region": "upper", "sort_order": 3},
        {"name": "جلوبازو", "name_en": "Biceps", "icon": "💪", "body_region": "upper", "sort_order": 4},
        {"name": "پشت‌بازو", "name_en": "Triceps", "icon": "💪", "body_region": "upper", "sort_order": 5},
        {"name": "ساعد", "name_en": "Forearms", "icon": "🤚", "body_region": "upper", "sort_order": 6},
        {"name": "چهارسر ران", "name_en": "Quadriceps", "icon": "🦵", "body_region": "lower", "sort_order": 7},
        {"name": "همسترینگ", "name_en": "Hamstrings", "icon": "🦵", "body_region": "lower", "sort_order": 8},
        {"name": "سرینی", "name_en": "Glutes", "icon": "🍑", "body_region": "lower", "sort_order": 9},
        {"name": "ساق پا", "name_en": "Calves", "icon": "🦶", "body_region": "lower", "sort_order": 10},
        {"name": "شکم", "name_en": "Abs", "icon": "🎯", "body_region": "core", "sort_order": 11},
    ]
    
    for group_data in groups:
        group = MuscleGroup(**group_data)
        db.add(group)
    
    db.commit()
    print("✅ گروه‌های عضلانی ایجاد شد")


def create_sample_exercises(db: Session) -> None:
    """ایجاد نمونه تمرینات (Idempotent)"""
    # بررسی وجود حداقل یک تمرین
    existing = db.query(Exercise).first()
    if existing:
        print("ℹ️  نمونه تمرینات از قبل موجود هستند")
        return
    
    chest = db.query(MuscleGroup).filter(MuscleGroup.name == "سینه").first()
    back = db.query(MuscleGroup).filter(MuscleGroup.name == "پشت").first()
    legs = db.query(MuscleGroup).filter(MuscleGroup.name == "چهارسر ران").first()
    
    if not all([chest, back, legs]):
        return
    
    # تمرینات سینه
    chest_exercises = [
        {"name": "پرس سینه هالتر", "name_en": "Barbell Bench Press", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "پرس سینه دمبل", "name_en": "Dumbbell Bench Press", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "فلای دمبل", "name_en": "Dumbbell Fly", "is_compound": False, "type": ExerciseType.RESISTANCE},
        {"name": "پرس بالاسینه", "name_en": "Incline Bench Press", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "کراس اور کابل", "name_en": "Cable Crossover", "is_compound": False, "type": ExerciseType.RESISTANCE},
    ]
    
    for ex_data in chest_exercises:
        ex = Exercise(muscle_group_id=chest.id, **ex_data)
        db.add(ex)
    
    # تمرینات پشت
    back_exercises = [
        {"name": "بارفیکس", "name_en": "Pull-up", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "زیربغل سیم‌کش", "name_en": "Lat Pulldown", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "رویینگ هالتر خم", "name_en": "Bent Over Row", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "رویینگ دمبل تک‌دست", "name_en": "Single Arm Row", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "ددلیفت", "name_en": "Deadlift", "is_compound": True, "is_risky": True, "type": ExerciseType.RESISTANCE},
    ]
    
    for ex_data in back_exercises:
        ex = Exercise(muscle_group_id=back.id, **ex_data)
        db.add(ex)
    
    # تمرینات پا
    leg_exercises = [
        {"name": "اسکات هالتر", "name_en": "Barbell Squat", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "لگ پرس", "name_en": "Leg Press", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "لانج دمبل", "name_en": "Dumbbell Lunges", "is_compound": True, "type": ExerciseType.RESISTANCE},
        {"name": "جلو پا ماشین", "name_en": "Leg Extension", "is_compound": False, "type": ExerciseType.RESISTANCE},
        {"name": "پشت پا خوابیده", "name_en": "Lying Leg Curl", "is_compound": False, "type": ExerciseType.RESISTANCE},
    ]
    
    for ex_data in leg_exercises:
        ex = Exercise(muscle_group_id=legs.id, **ex_data)
        db.add(ex)
    
    db.commit()
    print("✅ نمونه تمرینات ایجاد شد")


def create_supplement_categories(db: Session) -> None:
    """ایجاد دسته‌بندی‌های مکمل (Idempotent)"""
    # بررسی وجود حداقل یک دسته‌بندی
    existing = db.query(SupplementCategory).first()
    if existing:
        print("ℹ️  دسته‌بندی‌های مکمل از قبل موجود هستند")
        return
    
    categories = [
        {"name": "پروتئین‌ها", "name_en": "Proteins", "icon": "💪", "sort_order": 1},
        {"name": "کراتین", "name_en": "Creatine", "icon": "⚡", "sort_order": 2},
        {"name": "پیش‌تمرین", "name_en": "Pre-Workout", "icon": "🔥", "sort_order": 3},
        {"name": "آمینو اسیدها", "name_en": "Amino Acids", "icon": "🧬", "sort_order": 4},
        {"name": "ویتامین و مواد معدنی", "name_en": "Vitamins & Minerals", "icon": "💊", "sort_order": 5},
        {"name": "چربی‌سوزها", "name_en": "Fat Burners", "icon": "🔥", "sort_order": 6},
        {"name": "سایر", "name_en": "Others", "icon": "📦", "sort_order": 7},
    ]
    
    for cat_data in categories:
        category = SupplementCategory(**cat_data)
        db.add(category)
    
    db.commit()
    print("✅ دسته‌بندی‌های مکمل ایجاد شد")


def init_db(db: Session) -> None:
    """
    راه‌اندازی کامل دیتابیس (Idempotent)
    =====================================
    این تابع می‌تواند چندین بار اجرا شود بدون ایجاد مشکل
    در هر اجرا فقط داده‌های ضروری که وجود ندارند ایجاد می‌شوند
    """
    print("🚀 شروع راه‌اندازی دیتابیس...")
    
    try:
        # ایجاد جداول (SQLAlchemy خودش بررسی می‌کند که وجود دارند یا نه)
        create_tables()
        
        # ایجاد داده‌های اولیه (هر تابع idempotent است)
        create_default_user(db)
        create_food_categories(db)
        create_sample_foods(db)
        create_muscle_groups(db)
        create_sample_exercises(db)
        create_supplement_categories(db)
        
        print("✅ راه‌اندازی دیتابیس با موفقیت انجام شد!")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی دیتابیس: {e}")
        db.rollback()
        raise


if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
