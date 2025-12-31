# 🏋️ FLEX PRO Backend

سیستم هوشمند مدیریت مربیگری ورزشی - Backend API

## 🚀 ویژگی‌ها

- ✅ **FastAPI** - فریمورک مدرن و سریع
- ✅ **SQLAlchemy** - ORM قدرتمند
- ✅ **JWT Authentication** - احراز هویت امن
- ✅ **Pydantic** - اعتبارسنجی داده‌ها
- ✅ **محاسبات تغذیه** - BMR, TDEE, ماکروها
- ✅ **موتور تمرینی** - پیشنهاد برنامه، محاسبه 1RM
- ✅ **API مستند** - Swagger UI + ReDoc

## 📦 نصب و راه‌اندازی

### 1. ایجاد محیط مجازی

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 3. تنظیم متغیرهای محیطی

```bash
cp .env.example .env
# ویرایش .env و تنظیم SECRET_KEY
```

### 4. اجرای سرور

```bash
python run.py
```

یا:

```bash
uvicorn app.main:app --reload
```

### 5. مشاهده مستندات

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 ساختار پروژه

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry Point
│   ├── config.py            # تنظیمات
│   │
│   ├── api/                 # API Routes
│   │   ├── deps.py          # وابستگی‌ها
│   │   └── v1/
│   │       ├── router.py
│   │       ├── auth.py      # احراز هویت
│   │       ├── users.py
│   │       ├── athletes.py
│   │       ├── foods.py
│   │       ├── exercises.py
│   │       ├── training.py
│   │       ├── diet.py
│   │       └── calculator.py
│   │
│   ├── core/                # هسته منطقی
│   │   ├── security.py      # JWT & Hashing
│   │   ├── calculator.py    # محاسبات تغذیه
│   │   ├── training_engine.py
│   │   └── diet_engine.py
│   │
│   ├── models/              # مدل‌های دیتابیس
│   │   ├── user.py
│   │   ├── athlete.py
│   │   ├── food.py
│   │   ├── exercise.py
│   │   ├── training.py
│   │   ├── diet.py
│   │   └── ...
│   │
│   ├── schemas/             # Pydantic Schemas
│   │   └── ...
│   │
│   ├── services/            # Business Logic
│   │   └── ...
│   │
│   └── db/                  # دیتابیس
│       ├── base.py
│       ├── session.py
│       └── init_db.py
│
├── requirements.txt
├── run.py
└── README.md
```

## 🔌 API Endpoints

### 🔐 احراز هویت
| Method | Endpoint | توضیح |
|--------|----------|-------|
| POST | `/api/v1/auth/register` | ثبت‌نام |
| POST | `/api/v1/auth/login` | ورود |
| POST | `/api/v1/auth/refresh` | تمدید توکن |
| GET | `/api/v1/auth/me` | اطلاعات کاربر |

### 🏋️ شاگردان
| Method | Endpoint | توضیح |
|--------|----------|-------|
| GET | `/api/v1/athletes` | لیست شاگردان |
| POST | `/api/v1/athletes` | ایجاد شاگرد |
| GET | `/api/v1/athletes/{id}` | جزئیات شاگرد |
| PUT | `/api/v1/athletes/{id}` | ویرایش |
| DELETE | `/api/v1/athletes/{id}` | حذف |
| GET | `/api/v1/athletes/{id}/nutrition` | محاسبه تغذیه |

### 🍎 غذاها
| Method | Endpoint | توضیح |
|--------|----------|-------|
| GET | `/api/v1/foods/categories` | دسته‌بندی‌ها |
| GET | `/api/v1/foods/search` | جستجو |
| GET | `/api/v1/foods/{id}/calculate` | محاسبه ماکرو |

### 💪 تمرینات
| Method | Endpoint | توضیح |
|--------|----------|-------|
| GET | `/api/v1/exercises/muscle-groups` | گروه‌های عضلانی |
| GET | `/api/v1/exercises/search` | جستجو |

### 🧮 محاسبات
| Method | Endpoint | توضیح |
|--------|----------|-------|
| POST | `/api/v1/calculator/bmr` | محاسبه BMR |
| POST | `/api/v1/calculator/tdee` | محاسبه TDEE |
| POST | `/api/v1/calculator/macros` | محاسبه ماکروها |
| POST | `/api/v1/calculator/1rm` | تخمین 1RM |

## 🔧 توسعه

### اجرای تست‌ها

```bash
pytest
```

### Migration دیتابیس

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 📝 نکات مهم

1. **امنیت**: SECRET_KEY را در production تغییر دهید
2. **دیتابیس**: برای production از PostgreSQL استفاده کنید
3. **CORS**: origin های مجاز را محدود کنید

## 📄 لایسنس

این پروژه خصوصی است.
