"""
FLEX PRO Backend
================
سیستم هوشمند مدیریت مربیگری ورزشی

Main Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.api.v1.router import api_router
from app.db.session import SessionLocal
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle event handler
    اجرا در شروع و پایان اپلیکیشن
    """
    # Startup: راه‌اندازی دیتابیس
    print("🚀 Starting FLEX PRO Backend...")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    
    yield
    
    # Shutdown
    print("👋 Shutting down FLEX PRO Backend...")


# ایجاد اپلیکیشن FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",           # Swagger UI
    redoc_url="/redoc",         # ReDoc
    openapi_url="/openapi.json",
)


# ===== Middleware =====

# CORS - اجازه دسترسی از فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Exception Handlers =====

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    هندلر خطاهای اعتبارسنجی
    تبدیل خطاها به فرمت فارسی
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "خطا در اعتبارسنجی داده‌ها",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    هندلر خطاهای عمومی
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "خطای داخلی سرور",
            "message": str(exc) if settings.DEBUG else "لطفاً بعداً تلاش کنید"
        }
    )


# ===== Routes =====

# روت اصلی API
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)


# روت سلامت سرور
@app.get("/", tags=["🏠 Root"])
def root():
    """
    صفحه اصلی API
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "status": "running ✅"
    }


@app.get("/health", tags=["🏥 Health"])
def health_check():
    """
    بررسی سلامت سرور
    """
    return {
        "status": "healthy",
        "database": "connected",
    }


# ===== Run =====

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1
    )
