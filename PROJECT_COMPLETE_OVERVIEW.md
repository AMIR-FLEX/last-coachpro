# 📊 نمای کامل پروژه FLEX PRO

## 🎯 معرفی پروژه

**FLEX PRO** یک سیستم جامع و هوشمند مدیریت مربیگری ورزشی است که شامل مدیریت کامل برنامه‌های تمرینی، تغذیه، مکمل‌ها و پیگیری پیشرفت شاگردان می‌باشد.

**نسخه:** 1.0.0  
**تاریخ بروزرسانی:** 2024  
**وضعیت:** Production Ready ✅

---

## 🏗️ معماری پروژه

پروژه به صورت **Full-Stack** با جداسازی کامل Frontend و Backend طراحی شده است:

```
┌─────────────────────────────────────────────────┐
│           Frontend (Next.js 14)                 │
│  ┌─────────────┐  ┌──────────────┐            │
│  │  Pages      │  │  Components  │            │
│  │  (App Router)│  │  (TypeScript)│            │
│  └─────────────┘  └──────────────┘            │
│         │                  │                   │
│         └────────┬─────────┘                   │
│                  │                             │
│         ┌────────▼─────────┐                   │
│         │   API Client     │                   │
│         │   (Axios)        │                   │
│         └────────┬─────────┘                   │
└──────────────────┼─────────────────────────────┘
                   │ HTTP/REST
                   │ (JWT Auth)
┌──────────────────▼─────────────────────────────┐
│         Backend (FastAPI)                      │
│  ┌──────────────┐  ┌──────────────┐           │
│  │   API Routes │  │   Services   │           │
│  │   (v1)       │  │   (Business) │           │
│  └──────────────┘  └──────────────┘           │
│         │                  │                   │
│         └────────┬─────────┘                   │
│                  │                             │
│         ┌────────▼─────────┐                   │
│         │   SQLAlchemy     │                   │
│         │   (ORM)          │                   │
│         └────────┬─────────┘                   │
│                  │                             │
│         ┌────────▼─────────┐                   │
│         │   SQLite DB      │                   │
│         │   (Production:   │                   │
│         │   PostgreSQL)    │                   │
│         └──────────────────┘                   │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ تکنولوژی‌های استفاده شده

### Frontend

| تکنولوژی | نسخه | استفاده |
|---------|------|---------|
| **Next.js** | 14.2.5 | Framework اصلی |
| **React** | 18.3.1 | UI Library |
| **TypeScript** | 5.4.5 | Type Safety |
| **Tailwind CSS** | 3.4.7 | Styling |
| **Zustand** | 4.5.2 | State Management |
| **React Query** | 5.28.9 | Server State & Caching |
| **Axios** | 1.7.2 | HTTP Client |
| **Chart.js** | 4.4.2 | نمودارها |
| **Framer Motion** | 11.0.8 | انیمیشن‌ها |
| **html2canvas** | 1.4.1 | Print/PDF |
| **jsPDF** | 2.5.1 | PDF Generation |
| **Lucide React** | 0.263.1 | Icons |
| **React Hot Toast** | 2.4.1 | Notifications |
| **SweetAlert2** | 11.10.3 | Alert Dialogs |
| **DnD Kit** | 6.1.0 | Drag & Drop |

### Backend

| تکنولوژی | نسخه | استفاده |
|---------|------|---------|
| **FastAPI** | 0.115.6 | Web Framework |
| **SQLAlchemy** | 2.0.36 | ORM |
| **Pydantic** | 2.10.4 | Data Validation |
| **Uvicorn** | 0.34.0 | ASGI Server |
| **JWT (python-jose)** | 3.3.0 | Authentication |
| **Bcrypt** | 4.2.1 | Password Hashing |
| **Alembic** | 1.14.0 | Database Migrations |
| **SQLite** | - | Database (Dev) |
| **Pytest** | 8.3.4 | Testing |

---

## 📁 ساختار کامل پروژه

```
LAST COACH APP/
│
├── 📁 app/                          # Next.js App Router
│   ├── dashboard/                   # صفحات داشبورد
│   │   ├── athletes/               # مدیریت شاگردان
│   │   │   ├── [id]/              # صفحه جزئیات شاگرد (Dynamic Route)
│   │   │   │   ├── page.tsx       # نمایش پنل‌ها
│   │   │   │   └── edit/
│   │   │   │       └── page.tsx   # ویرایش شاگرد
│   │   │   └── new/
│   │   │       └── page.tsx       # ایجاد شاگرد جدید
│   │   ├── layout.tsx             # Layout داشبورد (Header + Sidebar)
│   │   └── page.tsx               # صفحه اصلی (لیست شاگردان)
│   ├── login/
│   │   └── page.tsx               # صفحه ورود
│   ├── globals.css                # استایل‌های سراسری
│   ├── layout.tsx                 # Root Layout
│   └── page.tsx                   # صفحه اصلی (Redirect)
│
├── 📁 components/                  # کامپوننت‌های React (TypeScript)
│   ├── diet-panel.tsx            # پنل برنامه تغذیه
│   ├── header.tsx                # هدر نوار بالا
│   ├── print-modal.tsx           # مودال چاپ/PDF
│   ├── profile-panel.tsx         # پنل پروفایل و پیشرفت
│   ├── providers.tsx             # React Query Provider
│   ├── sidebar.tsx               # منوی کناری
│   ├── supplements-panel.tsx     # پنل برنامه مکمل
│   ├── training-panel.tsx        # پنل برنامه تمرینی
│   ├── user-list.tsx             # لیست شاگردان
│   └── user-modal.tsx            # فرم ایجاد/ویرایش شاگرد
│
├── 📁 data/                       # داده‌های تمرینات و غذاها
│   ├── cardioExercises.ts        # تمرینات کاردیو
│   ├── correctiveExercises.ts    # تمرینات اصلاحی
│   ├── foodData.ts               # بانک غذاها
│   ├── resistanceExercises.ts    # تمرینات مقاومتی
│   ├── supplementsData.ts        # بانک مکمل‌ها
│   └── warmupCooldown.ts         # گرم کردن/سرد کردن
│
├── 📁 lib/                        # کتابخانه‌ها و توابع کمکی
│   ├── api-client.ts             # API Client (Axios) - تمام API calls
│   └── utils.ts                  # توابع کمکی (format, calculate, etc.)
│
├── 📁 store/                      # Zustand Stores
│   ├── app-store.ts              # State مدیریت (Theme, Tab, Active Athlete)
│   └── auth-store.ts             # State احراز هویت (User, Token)
│
├── 📁 types/                      # TypeScript Types
│   └── index.ts                  # تمام Type Definitions
│
├── 📁 backend/                    # Backend (FastAPI)
│   ├── 📁 app/                   # کد اصلی Backend
│   │   ├── api/                  # API Routes
│   │   │   ├── deps.py          # Dependencies (get_db, get_current_user)
│   │   │   └── v1/              # API Version 1
│   │   │       ├── auth.py      # 🔐 احراز هویت
│   │   │       ├── users.py     # 👤 مدیریت کاربران
│   │   │       ├── athletes.py  # 🏋️ مدیریت شاگردان
│   │   │       ├── foods.py     # 🍎 بانک غذاها
│   │   │       ├── exercises.py # 💪 بانک تمرینات
│   │   │       ├── training.py  # 📋 برنامه تمرینی
│   │   │       ├── diet.py      # 🥗 برنامه غذایی
│   │   │       ├── supplement_plan.py # 💊 برنامه مکمل
│   │   │       ├── calculator.py # 🧮 محاسبات (BMR, TDEE, Macros)
│   │   │       └── router.py    # Router اصلی
│   │   ├── core/                 # موتورهای اصلی
│   │   │   ├── calculator.py    # محاسبات تغذیه (BMR, TDEE, Macros)
│   │   │   ├── diet_engine.py   # موتور تغذیه (توزیع ماکروها)
│   │   │   ├── security.py      # امنیت (JWT, Password Hashing)
│   │   │   └── training_engine.py # موتور تمرین (1RM, پیشنهاد Split)
│   │   ├── db/                   # Database
│   │   │   ├── base.py          # Base Model
│   │   │   ├── init_db.py       # Initialize Database
│   │   │   ├── migrate_data.py  # Migrate Data (Foods, Exercises, Supplements)
│   │   │   └── session.py       # Database Session
│   │   ├── models/               # SQLAlchemy Models (Database Tables)
│   │   │   ├── user.py          # جدول کاربران
│   │   │   ├── athlete.py       # جدول شاگردان + Injuries + Measurements
│   │   │   ├── food.py          # جداول غذاها و دسته‌بندی‌ها
│   │   │   ├── exercise.py      # جداول تمرینات و گروه‌های عضلانی
│   │   │   ├── supplement.py    # جداول مکمل‌ها و دسته‌بندی‌ها
│   │   │   ├── training.py      # جداول برنامه تمرینی
│   │   │   ├── diet.py          # جداول برنامه غذایی
│   │   │   ├── supplement_plan.py # جداول برنامه مکمل
│   │   │   └── progress.py      # جدول پیشرفت
│   │   ├── schemas/              # Pydantic Schemas (Request/Response)
│   │   │   ├── user.py          # User Schemas
│   │   │   ├── athlete.py       # Athlete Schemas
│   │   │   ├── food.py          # Food Schemas
│   │   │   ├── exercise.py      # Exercise Schemas
│   │   │   ├── training.py      # Training Plan Schemas
│   │   │   ├── diet.py          # Diet Plan Schemas
│   │   │   ├── supplement_plan.py # Supplement Plan Schemas
│   │   │   └── common.py        # Common Schemas (Pagination, etc.)
│   │   ├── services/             # Business Logic Layer
│   │   │   ├── user_service.py  # منطق کاربران
│   │   │   ├── athlete_service.py # منطق شاگردان
│   │   │   ├── food_service.py  # منطق غذاها
│   │   │   ├── exercise_service.py # منطق تمرینات
│   │   │   ├── training_service.py # منطق برنامه تمرینی
│   │   │   ├── diet_service.py  # منطق برنامه غذایی
│   │   │   └── supplement_plan_service.py # منطق برنامه مکمل
│   │   ├── config.py             # تنظیمات (Environment Variables)
│   │   └── main.py               # Entry Point (FastAPI App)
│   ├── 📁 data/                  # داده‌های JSON
│   │   ├── exercises.json       # 281 تمرین
│   │   ├── foods.json           # 254 غذا
│   │   └── supplements.json     # 124 مکمل
│   ├── requirements.txt          # Python Dependencies
│   ├── requirements-fix.txt      # Dependencies بدون orjson (Python 3.14)
│   ├── run.py                    # اجرای سرور
│   └── README.md                 # راهنمای Backend
│
├── 📁 public/                     # فایل‌های استاتیک
│
├── ⚙️ فایل‌های تنظیمات
│   ├── package.json              # Dependencies Frontend
│   ├── next.config.js            # تنظیمات Next.js
│   ├── tailwind.config.ts        # تنظیمات Tailwind
│   ├── tsconfig.json             # تنظیمات TypeScript
│   ├── postcss.config.js         # تنظیمات PostCSS
│   ├── eslint.config.js          # تنظیمات ESLint
│   └── .npmrc                    # تنظیمات npm (legacy-peer-deps)
│
├── 🔧 فایل‌های اجرایی
│   ├── start-full-project.bat    # اجرای کامل پروژه (Windows)
│   ├── start-full-project.ps1    # اجرای کامل پروژه (PowerShell)
│   ├── fix-python-314.bat        # حل مشکل Python 3.14
│   ├── push-to-github.bat        # Push به GitHub
│   ├── push-to-github.ps1        # Push به GitHub (PowerShell)
│   └── test-run.bat              # تست پروژه
│
└── 📖 مستندات
    ├── README.md                  # راهنمای اصلی
    ├── README_QUICK_START.md      # راهنمای سریع
    ├── START_PROJECT_FULL.md      # راهنمای کامل اجرا
    ├── INSTALL_PYTHON_313.md      # نصب Python 3.13
    ├── SOLVE_PYTHON_314.md        # حل مشکل Python 3.14
    ├── PROJECT_STRUCTURE.md       # ساختار پروژه
    └── PROJECT_COMPLETE_OVERVIEW.md # این فایل (نمای کامل)
```

---

## 🔌 API Endpoints (Backend)

### 🔐 احراز هویت (`/api/v1/auth`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| POST | `/register` | ثبت‌نام کاربر جدید |
| POST | `/login` | ورود به سیستم (دریافت JWT) |
| POST | `/refresh` | تازه‌سازی Access Token |
| POST | `/logout` | خروج از سیستم |

**Request Example (Login):**
```json
POST /api/v1/auth/login
{
  "email": "admin@flexpro.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 👤 کاربران (`/api/v1/users`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/me` | دریافت پروفایل کاربر فعلی |
| PUT | `/me` | بروزرسانی پروفایل |
| GET | `/me/stats` | آمار کاربر |

### 🏋️ شاگردان (`/api/v1/athletes`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/` | لیست شاگردان (با Pagination) |
| POST | `/` | ایجاد شاگرد جدید |
| GET | `/{id}` | جزئیات شاگرد |
| PUT | `/{id}` | بروزرسانی شاگرد |
| DELETE | `/{id}` | حذف شاگرد |
| GET | `/{id}/stats` | آمار شاگرد |
| POST | `/{id}/injuries` | اضافه کردن آسیب |
| DELETE | `/{id}/injuries/{injury_id}` | حذف آسیب |
| POST | `/{id}/measurements` | اضافه کردن اندازه‌گیری |
| GET | `/{id}/measurements` | لیست اندازه‌گیری‌ها |

**Request Example (Create Athlete):**
```json
POST /api/v1/athletes
{
  "name": "علی احمدی",
  "age": 28,
  "gender": "male",
  "height": 175,
  "weight": 75,
  "goal": "bulk",
  "activity_level": "active",
  "experience_level": "intermediate"
}
```

### 🍎 بانک غذاها (`/api/v1/foods`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/categories` | لیست دسته‌بندی‌ها |
| GET | `/categories/with-foods` | دسته‌بندی‌ها با غذاها |
| GET | `/` | لیست غذاها (با جستجو و فیلتر) |
| GET | `/{id}` | جزئیات غذا |
| POST | `/` | اضافه کردن غذا جدید |
| PUT | `/{id}` | بروزرسانی غذا |
| DELETE | `/{id}` | حذف غذا |
| GET | `/search` | جستجوی غذا |
| POST | `/calculate-macros` | محاسبه ماکروهای غذا |

### 💪 بانک تمرینات (`/api/v1/exercises`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/muscle-groups` | لیست گروه‌های عضلانی |
| GET | `/muscle-groups/with-exercises` | گروه‌ها با تمرینات |
| GET | `/` | لیست تمرینات (با فیلتر) |
| GET | `/{id}` | جزئیات تمرین |
| POST | `/` | اضافه کردن تمرین جدید |
| GET | `/search` | جستجوی تمرین |

### 📋 برنامه تمرینی (`/api/v1/training`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/athletes/{athlete_id}/plans` | لیست برنامه‌های تمرینی شاگرد |
| GET | `/athletes/{athlete_id}/plans/active` | برنامه فعال |
| POST | `/athletes/{athlete_id}/plans` | ایجاد برنامه جدید |
| GET | `/plans/{plan_id}` | جزئیات برنامه |
| PUT | `/plans/{plan_id}` | بروزرسانی برنامه |
| DELETE | `/plans/{plan_id}` | حذف برنامه |
| POST | `/plans/{plan_id}/activate` | فعال‌سازی برنامه |
| POST | `/plans/{plan_id}/days` | اضافه کردن روز تمرین |
| DELETE | `/plans/{plan_id}/days/{day_id}` | حذف روز |
| POST | `/plans/{plan_id}/days/{day_id}/items` | اضافه کردن آیتم تمرین |
| PUT | `/plans/{plan_id}/days/{day_id}/items/{item_id}` | بروزرسانی آیتم |
| DELETE | `/plans/{plan_id}/days/{day_id}/items/{item_id}` | حذف آیتم |
| POST | `/plans/{plan_id}/days/{day_id}/items/reorder` | مرتب‌سازی آیتم‌ها |

### 🥗 برنامه غذایی (`/api/v1/diet`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/athletes/{athlete_id}/plans` | لیست برنامه‌های غذایی |
| GET | `/athletes/{athlete_id}/plans/active` | برنامه فعال |
| POST | `/athletes/{athlete_id}/plans` | ایجاد برنامه جدید |
| GET | `/plans/{plan_id}` | جزئیات برنامه |
| PUT | `/plans/{plan_id}` | بروزرسانی برنامه |
| DELETE | `/plans/{plan_id}` | حذف برنامه |
| POST | `/plans/{plan_id}/activate` | فعال‌سازی برنامه |
| POST | `/plans/{plan_id}/items` | اضافه کردن آیتم غذایی |
| DELETE | `/plans/{plan_id}/items/{item_id}` | حذف آیتم |
| POST | `/plans/{plan_id}/items/reorder` | مرتب‌سازی آیتم‌ها |

### 💊 برنامه مکمل (`/api/v1/supplement-plans`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| GET | `/athletes/{athlete_id}/plans` | لیست برنامه‌های مکمل |
| GET | `/athletes/{athlete_id}/plans/active` | برنامه فعال |
| POST | `/athletes/{athlete_id}/plans` | ایجاد برنامه جدید |
| GET | `/plans/{plan_id}` | جزئیات برنامه |
| PUT | `/plans/{plan_id}` | بروزرسانی برنامه |
| DELETE | `/plans/{plan_id}` | حذف برنامه |
| POST | `/plans/{plan_id}/activate` | فعال‌سازی برنامه |
| POST | `/plans/{plan_id}/items` | اضافه کردن مکمل |
| DELETE | `/plans/{plan_id}/items/{item_id}` | حذف مکمل |

### 🧮 محاسبات (`/api/v1/calculator`)

| Method | Endpoint | توضیحات |
|--------|----------|---------|
| POST | `/bmr` | محاسبه BMR (Basal Metabolic Rate) |
| POST | `/tdee` | محاسبه TDEE (Total Daily Energy Expenditure) |
| POST | `/macros` | محاسبه ماکروها (پروتئین، کربوهیدرات، چربی) |
| POST | `/ideal-weight` | محاسبه وزن ایده‌آل |
| POST | `/bmi` | محاسبه BMI |
| POST | `/body-fat` | تخمین درصد چربی بدن |
| POST | `/training/1rm` | محاسبه 1RM (One Rep Max) |
| POST | `/training/split-recommendation` | پیشنهاد Split تمرینی |

**Request Example (BMR):**
```json
POST /api/v1/calculator/bmr
{
  "weight": 75,
  "height": 175,
  "age": 28,
  "gender": "male",
  "body_fat": 15
}
```

**Response:**
```json
{
  "bmr": 1756.5,
  "method": "katch_mcardle",
  "formula": "Katch-McArdle (with body fat)"
}
```

---

## 🗄️ Database Schema (Models)

### 👤 User (کاربران)
- `id` (PK)
- `email` (Unique)
- `hashed_password`
- `full_name`
- `phone`
- `bio`
- `avatar_url`
- `is_active`
- `is_superuser`
- `theme`
- `language`
- `created_at`, `updated_at`

### 🏋️ Athlete (شاگردان)
- `id` (PK)
- `coach_id` (FK → User)
- `name`
- `age`, `gender`, `height`, `weight`
- `phone`, `email`
- `goal` (Enum: bulk, cut, maintain, etc.)
- `activity_level` (Enum: sedentary, light, etc.)
- `experience_level` (Enum: beginner, intermediate, etc.)
- `job`, `sleep_quality`
- `allergies`, `medical_conditions`, `notes`
- `is_active`
- `avatar_url`
- `subscription_start`, `subscription_months`, `subscription_amount`
- `created_at`, `updated_at`

### 🏋️ AthleteInjury (آسیب‌های شاگرد)
- `id` (PK)
- `athlete_id` (FK → Athlete)
- `body_part`
- `description`
- `severity`
- `occurred_at`
- `healed_at`

### 🏋️ AthleteMeasurement (اندازه‌گیری‌های شاگرد)
- `id` (PK)
- `athlete_id` (FK → Athlete)
- `recorded_at`
- `weight`
- `body_fat`
- `neck`, `chest`, `shoulders`, `waist`, `hip`
- `arm_right`, `arm_left`
- `thigh_right`, `thigh_left`
- `calf_right`, `calf_left`
- `wrist`

### 🍎 FoodCategory (دسته‌بندی غذاها)
- `id` (PK)
- `name`, `name_en`
- `icon`
- `sort_order`

### 🍎 Food (غذاها)
- `id` (PK)
- `category_id` (FK → FoodCategory)
- `name`, `name_en`
- `unit` (گرم، عدد، فنجان، ...)
- `base_amount`
- `calories`
- `protein`, `carbs`, `fat`, `fiber`
- `description`

### 💪 MuscleGroup (گروه‌های عضلانی)
- `id` (PK)
- `name`, `name_en`
- `icon`
- `body_region` (upper, lower, core)
- `sort_order`

### 💪 Exercise (تمرینات)
- `id` (PK)
- `muscle_group_id` (FK → MuscleGroup)
- `name`, `name_en`
- `type` (Enum: RESISTANCE, CARDIO, CORRECTIVE)
- `is_compound`
- `is_risky`
- `equipment` (Enum: BODYWEIGHT, DUMBBELL, etc.)
- `difficulty` (Enum: BEGINNER, INTERMEDIATE, ADVANCED)
- `description`
- `instructions` (JSON)
- `video_url`

### 💊 SupplementCategory (دسته‌بندی مکمل‌ها)
- `id` (PK)
- `name`, `name_en`
- `icon`
- `sort_order`

### 💊 Supplement (مکمل‌ها)
- `id` (PK)
- `category_id` (FK → SupplementCategory)
- `name`, `name_en`
- `description`
- `benefits` (JSON Array)
- `dosage_info`
- `timing_recommendations` (JSON Array)

### 📋 TrainingPlan (برنامه تمرینی)
- `id` (PK)
- `athlete_id` (FK → Athlete)
- `name`
- `is_active`
- `start_date`, `end_date`
- `notes`
- `created_at`, `updated_at`

### 📋 TrainingDay (روز تمرین)
- `id` (PK)
- `plan_id` (FK → TrainingPlan)
- `day_number` (1-7)
- `name` (اختیاری)
- `notes`

### 📋 WorkoutItem (آیتم تمرین)
- `id` (PK)
- `day_id` (FK → TrainingDay)
- `exercise_id` (FK → Exercise, اختیاری)
- `type` (RESISTANCE, CARDIO, CORRECTIVE, WARMUP, COOLDOWN)
- `custom_name` (برای تمرینات سفارشی)
- `sets`, `reps` (برای مقاومتی)
- `duration`, `intensity` (برای کاردیو)
- `rest` (ثانیه یا دقیقه)
- `weight`, `tempo`, `drop_count` (برای سیستم‌های پیشرفته)
- `notes`
- `order`

### 🥗 DietPlan (برنامه غذایی)
- `id` (PK)
- `athlete_id` (FK → Athlete)
- `name`
- `is_active`
- `target_calories`
- `target_protein`, `target_carbs`, `target_fat`
- `start_date`, `end_date`
- `notes`
- `created_at`, `updated_at`

### 🥗 DietItem (آیتم غذایی)
- `id` (PK)
- `plan_id` (FK → DietPlan)
- `food_id` (FK → Food, اختیاری)
- `custom_name` (برای غذاهای سفارشی)
- `meal_type` (BREAKFAST, LUNCH, DINNER, SNACK, PRE_WORKOUT, POST_WORKOUT)
- `amount` (بر اساس unit غذا)
- `calories`, `protein`, `carbs`, `fat` (محاسبه شده)
- `notes`
- `order`

### 💊 SupplementPlan (برنامه مکمل)
- `id` (PK)
- `athlete_id` (FK → Athlete)
- `name`
- `is_active`
- `notes`
- `created_at`, `updated_at`

### 💊 SupplementPlanItem (آیتم مکمل)
- `id` (PK)
- `plan_id` (FK → SupplementPlan)
- `supplement_id` (FK → Supplement, اختیاری)
- `custom_name` (برای مکمل‌های سفارشی)
- `dose`
- `timing` (ناشتا، صبحانه، قبل تمرین، ...)
- `notes`
- `instructions`
- `order`

### 📊 ProgressRecord (پیشرفت)
- `id` (PK)
- `athlete_id` (FK → Athlete)
- `recorded_at`
- `weight`
- `body_fat`
- `measurements` (JSON)
- `notes`
- `photos` (JSON Array)

---

## 🎨 Frontend Components

### 📄 Pages (Next.js App Router)

#### `app/page.tsx` - صفحه اصلی
- Redirect به `/login` یا `/dashboard` بر اساس authentication

#### `app/login/page.tsx` - صفحه ورود
- فرم ورود با ایمیل و رمز عبور
- استفاده از `useAuthStore` برای login
- Redirect به `/dashboard` پس از ورود موفق

#### `app/dashboard/page.tsx` - صفحه اصلی داشبورد
- نمایش `UserList` component
- لیست تمام شاگردان

#### `app/dashboard/layout.tsx` - Layout داشبورد
- شامل `Header` و `Sidebar`
- مدیریت Authentication
- مدیریت Theme (Dark/Light)
- Navigation بین Tab ها

#### `app/dashboard/athletes/[id]/page.tsx` - جزئیات شاگرد
- Dynamic Route برای نمایش اطلاعات شاگرد
- نمایش پنل‌ها بر اساس `currentTab`:
  - `training` → `TrainingPanel`
  - `nutrition` → `DietPanel`
  - `supplements` → `SupplementsPanel`
  - `progress` → `ProfilePanel`

#### `app/dashboard/athletes/new/page.tsx` - ایجاد شاگرد جدید
- نمایش `UserModal` در حالت ایجاد

#### `app/dashboard/athletes/[id]/edit/page.tsx` - ویرایش شاگرد
- نمایش `UserModal` در حالت ویرایش
- Load کردن داده‌های فعلی

### 🧩 Components

#### `UserList` (`components/user-list.tsx`)
- لیست شاگردان با جستجو
- استفاده از React Query برای fetch داده‌ها
- قابلیت حذف
- Navigation به صفحه جزئیات

#### `UserModal` (`components/user-modal.tsx`)
- فرم جامع ایجاد/ویرایش شاگرد
- شامل:
  - اطلاعات پایه (نام، سن، جنسیت، ...)
  - اطلاعات فیزیکی (قد، وزن، چربی بدن)
  - اندازه‌گیری‌ها (گردن، سینه، کمر، ...)
  - اهداف (bulk, cut, maintain)
  - سطح فعالیت و تجربه
  - آلرژی‌ها و شرایط پزشکی
  - آسیب‌ها
  - اطلاعات مالی (اشتراک)
- استفاده از `apiClient` برای create/update
- مدیریت injuries و measurements جداگانه

#### `TrainingPanel` (`components/training-panel.tsx`)
- مدیریت برنامه تمرینی
- Drag & Drop برای مرتب‌سازی تمرینات
- اضافه کردن تمرینات از بانک (مقاومتی، کاردیو، اصلاحی)
- سیستم‌های پیشرفته (Drop Set, Rest-Pause, Tempo)
- ذخیره در Backend
- استفاده از `apiClient` برای CRUD operations

#### `DietPanel` (`components/diet-panel.tsx`)
- مدیریت برنامه غذایی
- اضافه کردن غذا از بانک
- محاسبه خودکار کالری و ماکروها
- توزیع غذاها در وعده‌ها (صبحانه، ناهار، شام، ...)
- Drag & Drop برای مرتب‌سازی
- ذخیره در Backend

#### `SupplementsPanel` (`components/supplements-panel.tsx`)
- مدیریت برنامه مکمل
- انتخاب از بانک مکمل‌ها یا ایجاد سفارشی
- تعیین دوز و زمان مصرف
- ذخیره در Backend

#### `ProfilePanel` (`components/profile-panel.tsx`)
- نمایش پروفایل شاگرد
- نمودار پیشرفت وزن و چربی بدن (Chart.js)
- تاریخچه اندازه‌گیری‌ها
- نمایش آسیب‌ها

#### `Header` (`components/header.tsx`)
- نوار بالا
- اطلاعات شاگرد فعال
- دکمه تغییر تم
- دکمه خروج

#### `Sidebar` (`components/sidebar.tsx`)
- منوی کناری
- Tab Navigation
- دکمه‌های Backup/Restore/Reset

#### `PrintModal` (`components/print-modal.tsx`)
- نمایش Preview برای چاپ
- تولید PDF با jsPDF
- قابلیت چاپ برنامه تمرینی/غذایی

#### `Providers` (`components/providers.tsx`)
- React Query Provider
- مدیریت Theme (Dark/Light)

---

## 🔄 State Management

### Zustand Stores

#### `app-store.ts` - State مدیریت اپلیکیشن
```typescript
{
  theme: 'dark' | 'light',
  currentTab: 'users' | 'training' | 'nutrition' | 'supplements' | 'progress',
  activeAthleteId: number | null,
  activeAthlete: Athlete | null,
  
  setTheme(),
  setCurrentTab(),
  setActiveAthleteId(),
  setActiveAthlete(),
  toggleTheme()
}
```

#### `auth-store.ts` - State احراز هویت
```typescript
{
  user: User | null,
  isAuthenticated: boolean,
  isLoading: boolean,
  error: string | null,
  
  login(),
  logout(),
  register(),
  fetchCurrentUser(),
  clearError()
}
```
- استفاده از `zustand/middleware/persist` برای ذخیره در localStorage

---

## 🔐 Authentication Flow

1. کاربر ایمیل و رمز عبور را وارد می‌کند
2. Frontend درخواست به `/api/v1/auth/login` می‌فرستد
3. Backend اعتبارسنجی می‌کند و JWT Token برمی‌گرداند
4. Frontend Token را در `localStorage` ذخیره می‌کند
5. در تمام درخواست‌های بعدی، Token در Header `Authorization: Bearer <token>` ارسال می‌شود
6. Backend Token را verify می‌کند
7. در صورت انقضا، از Refresh Token استفاده می‌شود

---

## 🧮 موتورهای محاسباتی

### Nutrition Calculator (`backend/app/core/calculator.py`)

#### BMR (Basal Metabolic Rate)
- **Mifflin-St Jeor**: بدون درصد چربی
- **Katch-McArdle**: با درصد چربی (دقیق‌تر)

#### TDEE (Total Daily Energy Expenditure)
- `BMR × Activity Factor`
- Activity Factors:
  - Sedentary: 1.2
  - Light: 1.375
  - Moderate: 1.55
  - Active: 1.725
  - Very Active: 1.9

#### Macros Distribution
بر اساس Goal:
- **Bulk**: پروتئین بالا، کربوهیدرات بالا
- **Cut**: پروتئین بالا، چربی متوسط، کربوهیدرات پایین
- **Maintain**: توزیع متعادل
- **Recomp**: ترکیبی از Bulk و Cut

### Training Engine (`backend/app/core/training_engine.py`)

#### 1RM Calculation
فرمول‌های مختلف:
- Epley: `weight × (1 + reps/30)`
- Brzycki: `weight × (36 / (37 - reps))`
- Lombardi: `weight × reps^0.10`

#### Split Recommendation
بر اساس:
- سطح تجربه
- روزهای تمرین در هفته
- اهداف (قدرت، حجم، استقامت)

### Diet Engine (`backend/app/core/diet_engine.py`)

#### Macro Distribution
توزیع ماکروها در وعده‌ها:
- صبحانه: 25% کالری
- ناهار: 35% کالری
- شام: 30% کالری
- میان‌وعده: 10% کالری

---

## 📊 Database Statistics

| دسته | تعداد | توضیحات |
|------|-------|---------|
| 🍎 غذاها | 254 | 9 دسته‌بندی |
| 💪 تمرینات | 281 | 10 گروه عضلانی |
| 💊 مکمل‌ها | 124 | 16 دسته‌بندی |
| **مجموع** | **659** | **35 دسته‌بندی** |

---

## 🚀 نحوه اجرای پروژه

### روش سریع:
```bash
start-full-project.bat
```

### روش دستی:

#### Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python run.py
```

#### Frontend:
```bash
npm install
npm run dev
```

### آدرس‌ها:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔑 کاربر پیش‌فرض

```
Email: admin@flexpro.com
Password: admin123
```

---

## 📦 Dependencies اصلی

### Frontend:
- **Next.js 14.2.5**: Framework
- **React 18.3.1**: UI Library
- **TypeScript 5.4.5**: Type Safety
- **Zustand 4.5.2**: State Management
- **React Query 5.28.9**: Server State
- **Axios 1.7.2**: HTTP Client
- **Chart.js 4.4.2**: نمودارها
- **Tailwind CSS 3.4.7**: Styling

### Backend:
- **FastAPI 0.115.6**: Web Framework
- **SQLAlchemy 2.0.36**: ORM
- **Pydantic 2.10.4**: Validation
- **Uvicorn 0.34.0**: ASGI Server
- **JWT (python-jose) 3.3.0**: Auth

---

## 🎯 ویژگی‌های کلیدی

✅ **مدیریت کامل شاگردان**
- ایجاد، ویرایش، حذف
- ذخیره اطلاعات جامع (فیزیکی، پزشکی، مالی)
- ردیابی آسیب‌ها و اندازه‌گیری‌ها

✅ **برنامه تمرینی هوشمند**
- بانک 281 تمرین
- Drag & Drop برای مرتب‌سازی
- سیستم‌های پیشرفته (Drop Set, Rest-Pause, Tempo)
- محاسبه 1RM

✅ **برنامه غذایی دقیق**
- بانک 254 غذا
- محاسبه خودکار کالری و ماکروها
- توزیع در وعده‌ها

✅ **برنامه مکمل**
- بانک 124 مکمل
- تعیین دوز و زمان مصرف

✅ **محاسبات دقیق**
- BMR, TDEE
- توزیع ماکروها
- BMI, وزن ایده‌آل
- درصد چربی بدن

✅ **رابط کاربری مدرن**
- Dark/Light Mode
- Responsive Design
- انیمیشن‌های روان
- UI/UX بهینه

✅ **امنیت**
- JWT Authentication
- Password Hashing (Bcrypt)
- CORS Protection

✅ **مستندسازی**
- API Docs (Swagger UI)
- TypeScript Types
- کامنت‌های فارسی

---

## 📱 صفحات و Route ها

| Route | Component | توضیحات |
|-------|-----------|---------|
| `/` | Redirect | به `/login` یا `/dashboard` |
| `/login` | `LoginPage` | صفحه ورود |
| `/dashboard` | `DashboardPage` | لیست شاگردان |
| `/dashboard/athletes/new` | `UserModal` | ایجاد شاگرد جدید |
| `/dashboard/athletes/[id]` | `AthleteDetailPage` | جزئیات شاگرد |
| `/dashboard/athletes/[id]/edit` | `UserModal` | ویرایش شاگرد |

---

## 🔄 Data Flow

### ایجاد/ویرایش شاگرد:
```
UserModal (Form) 
  → apiClient.createAthlete() / updateAthlete()
  → POST/PUT /api/v1/athletes
  → Backend Service
  → Database
  → Response
  → React Query Invalidate
  → UI Update
```

### دریافت لیست شاگردان:
```
UserList Component
  → useQuery(['athletes'])
  → apiClient.getAthletes()
  → GET /api/v1/athletes
  → Backend Service
  → Database
  → Response
  → React Query Cache
  → UI Render
```

---

## 🎨 Theme System

- **Dark Mode**: حالت تیره (پیش‌فرض)
- **Light Mode**: حالت روشن
- ذخیره در `localStorage`
- استفاده از CSS Variables برای رنگ‌ها
- انتقال نرم بین Theme ها

---

## 📄 Print & PDF

- استفاده از `html2canvas` برای تبدیل HTML به تصویر
- استفاده از `jsPDF` برای تولید PDF
- قابلیت چاپ برنامه تمرینی و غذایی
- Preview قبل از چاپ

---

## 🗂️ Data Files

### Frontend (`data/`):
- `resistanceExercises.ts` - تمرینات مقاومتی
- `cardioExercises.ts` - تمرینات کاردیو
- `correctiveExercises.ts` - تمرینات اصلاحی
- `foodData.ts` - بانک غذاها
- `supplementsData.ts` - بانک مکمل‌ها
- `warmupCooldown.ts` - گرم کردن/سرد کردن

### Backend (`backend/data/`):
- `exercises.json` - 281 تمرین (برای migrate به DB)
- `foods.json` - 254 غذا (برای migrate به DB)
- `supplements.json` - 124 مکمل (برای migrate به DB)

---

## 🔧 Configuration Files

### Frontend:
- `next.config.js` - تنظیمات Next.js
- `tsconfig.json` - تنظیمات TypeScript
- `tailwind.config.ts` - تنظیمات Tailwind
- `postcss.config.js` - تنظیمات PostCSS
- `.npmrc` - تنظیمات npm (legacy-peer-deps)

### Backend:
- `backend/app/config.py` - تنظیمات Backend (Environment Variables)
- `.env` - متغیرهای محیطی (در .gitignore)

---

## 🌐 Environment Variables

### Backend (`backend/.env`):
```env
DATABASE_URL=sqlite:///./flexpro.db
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend:
- `NEXT_PUBLIC_API_URL=http://localhost:8000` (اختیاری)

---

## 📈 Performance Optimizations

✅ **React Query Caching**
- Cache کردن داده‌های fetch شده
- Stale Time: 1 دقیقه
- Automatic Refetch

✅ **Code Splitting**
- Next.js Automatic Code Splitting
- Lazy Loading Components

✅ **Image Optimization**
- Next.js Image Component

✅ **Database Indexing**
- Foreign Keys
- Unique Constraints

---

## 🧪 Testing

### Backend:
- `pytest` - Unit Tests
- `pytest-asyncio` - Async Tests

### Frontend:
- TypeScript برای Type Checking
- ESLint برای Code Quality

---

## 🚀 Deployment

### Frontend:
- **Vercel** (توصیه می‌شود)
- یا هر Hosting که Node.js را پشتیبانی کند

### Backend:
- **Python Anywhere**
- **Heroku**
- **DigitalOcean**
- **AWS EC2**
- یا هر سرور Python

### Database:
- **SQLite** (Development)
- **PostgreSQL** (Production - توصیه می‌شود)

---

## 📝 TODO / Future Features

- [ ] اضافه کردن Push Notifications
- [ ] اضافه کردن Chat بین Coach و Athlete
- [ ] اضافه کردن Video Upload برای تمرینات
- [ ] اضافه کردن Mobile App (React Native)
- [ ] اضافه کردن Analytics Dashboard
- [ ] اضافه کردن Export به Excel
- [ ] اضافه کردن Multi-language Support

---

## 📞 Support

برای سوالات و مشکلات:
- بررسی `README.md`
- بررسی `START_PROJECT_FULL.md`
- بررسی `SOLVE_PYTHON_314.md` (اگر مشکل Python دارید)

---

## 📄 License

این پروژه یک پروژه خصوصی است.

---

**آخرین بروزرسانی:** 2024  
**نسخه:** 1.0.0  
**وضعیت:** Production Ready ✅

---

*این مستند کامل ترین نمای پروژه FLEX PRO است و شامل تمام جزئیات فنی و عملیاتی می‌باشد.*

