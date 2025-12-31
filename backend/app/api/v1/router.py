"""
Main API Router
===============
روتر اصلی API v1
"""

from fastapi import APIRouter

from app.api.v1 import auth, users, athletes, foods, exercises, training, diet, calculator

# روتر اصلی
api_router = APIRouter()

# ثبت روترهای فرعی
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["🔐 احراز هویت"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["👤 کاربران"]
)

api_router.include_router(
    athletes.router,
    prefix="/athletes",
    tags=["🏋️ شاگردان"]
)

api_router.include_router(
    foods.router,
    prefix="/foods",
    tags=["🍎 بانک غذاها"]
)

api_router.include_router(
    exercises.router,
    prefix="/exercises",
    tags=["💪 بانک تمرینات"]
)

api_router.include_router(
    training.router,
    prefix="/training",
    tags=["📋 برنامه تمرینی"]
)

api_router.include_router(
    diet.router,
    prefix="/diet",
    tags=["🥗 برنامه غذایی"]
)

api_router.include_router(
    calculator.router,
    prefix="/calculator",
    tags=["🧮 محاسبات"]
)
