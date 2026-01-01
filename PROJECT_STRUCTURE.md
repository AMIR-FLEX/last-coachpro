# 📁 ساختار پروژه FLEX PRO

## 📂 ساختار کامل

```
LAST COACH APP/
│
├── 📁 app/                          # Next.js App Router
│   ├── dashboard/                   # صفحات داشبورد
│   │   ├── athletes/               # مدیریت شاگردان
│   │   │   ├── [id]/              # صفحه جزئیات شاگرد
│   │   │   │   ├── page.tsx
│   │   │   │   └── edit/
│   │   │   │       └── page.tsx
│   │   │   └── new/
│   │   │       └── page.tsx
│   │   ├── layout.tsx             # Layout داشبورد
│   │   └── page.tsx               # صفحه اصلی داشبورد
│   ├── login/                      # صفحه ورود
│   │   └── page.tsx
│   ├── globals.css                 # استایل‌های عمومی
│   ├── layout.tsx                  # Layout اصلی
│   └── page.tsx                    # صفحه اصلی (Redirect)
│
├── 📁 components/                  # کامپوننت‌های React (TypeScript)
│   ├── diet-panel.tsx             # پنل برنامه تغذیه
│   ├── header.tsx                 # هدر
│   ├── print-modal.tsx            # مودال چاپ/PDF
│   ├── profile-panel.tsx          # پنل پروفایل
│   ├── providers.tsx              # React Query Provider
│   ├── sidebar.tsx                # منوی کناری
│   ├── supplements-panel.tsx      # پنل برنامه مکمل
│   ├── training-panel.tsx         # پنل برنامه تمرینی
│   ├── user-list.tsx              # لیست شاگردان
│   └── user-modal.tsx             # فرم ایجاد/ویرایش شاگرد
│
├── 📁 data/                        # داده‌های تمرینات و غذاها
│   ├── cardioExercises.ts         # تمرینات کاردیو
│   ├── correctiveExercises.ts     # تمرینات اصلاحی
│   ├── foodData.ts                # داده‌های غذا
│   ├── resistanceExercises.ts     # تمرینات مقاومتی
│   ├── supplementsData.ts         # داده‌های مکمل
│   └── warmupCooldown.ts          # گرم کردن/سرد کردن
│
├── 📁 lib/                         # کتابخانه‌ها و توابع کمکی
│   ├── api-client.ts              # API Client (Axios)
│   └── utils.ts                   # توابع کمکی
│
├── 📁 store/                       # Zustand Stores
│   ├── app-store.ts               # State مدیریت (Theme, Tab, Athlete)
│   └── auth-store.ts              # State احراز هویت
│
├── 📁 types/                       # TypeScript Types
│   └── index.ts                   # تعاریف Type
│
├── 📁 backend/                     # Backend (FastAPI)
│   ├── 📁 app/                    # کد اصلی Backend
│   │   ├── api/                   # API Routes
│   │   │   ├── deps.py           # Dependencies
│   │   │   └── v1/               # API v1
│   │   │       ├── athletes.py   # Routes شاگردان
│   │   │       ├── auth.py       # Routes احراز هویت
│   │   │       ├── calculator.py # Routes محاسبات
│   │   │       ├── diet.py       # Routes تغذیه
│   │   │       ├── exercises.py  # Routes تمرینات
│   │   │       ├── foods.py      # Routes غذاها
│   │   │       ├── router.py     # Router اصلی
│   │   │       ├── supplement_plan.py # Routes مکمل
│   │   │       ├── training.py   # Routes تمرین
│   │   │       └── users.py      # Routes کاربران
│   │   ├── core/                  # موتورهای اصلی
│   │   │   ├── calculator.py     # محاسبات تغذیه (BMR, TDEE)
│   │   │   ├── diet_engine.py    # موتور تغذیه
│   │   │   ├── security.py       # امنیت (JWT)
│   │   │   └── training_engine.py # موتور تمرین
│   │   ├── db/                    # Database
│   │   │   ├── base.py           # Base Model
│   │   │   ├── init_db.py        # Initialize DB
│   │   │   ├── migrate_data.py   # Migrate Data
│   │   │   └── session.py        # DB Session
│   │   ├── models/                # SQLAlchemy Models
│   │   │   ├── athlete.py        # Model شاگرد
│   │   │   ├── diet.py           # Model تغذیه
│   │   │   ├── exercise.py       # Model تمرین
│   │   │   ├── food.py           # Model غذا
│   │   │   ├── progress.py       # Model پیشرفت
│   │   │   ├── supplement_plan.py # Model برنامه مکمل
│   │   │   ├── supplement.py     # Model مکمل
│   │   │   ├── training.py       # Model تمرین
│   │   │   └── user.py           # Model کاربر
│   │   ├── schemas/               # Pydantic Schemas
│   │   │   └── (فایل‌های schema)
│   │   ├── services/              # Business Logic
│   │   │   └── (فایل‌های service)
│   │   ├── config.py              # تنظیمات
│   │   └── main.py                # Entry Point
│   ├── 📁 data/                   # داده‌های JSON
│   │   ├── exercises.json
│   │   ├── foods.json
│   │   └── supplements.json
│   ├── requirements.txt           # Dependencies Python
│   ├── requirements-fix.txt       # Dependencies بدون orjson
│   ├── run.py                     # اجرای سرور
│   └── README.md                  # راهنمای Backend
│
├── 📁 public/                      # فایل‌های استاتیک
│
├── 📄 README.md                    # راهنمای اصلی پروژه ⭐
├── 📄 README_QUICK_START.md        # راهنمای سریع
├── 📄 START_PROJECT_FULL.md        # راهنمای کامل اجرا
├── 📄 INSTALL_PYTHON_313.md        # راهنمای نصب Python 3.13
├── 📄 SOLVE_PYTHON_314.md          # حل مشکل Python 3.14
│
├── 🔧 فایل‌های اجرایی
│   ├── start-full-project.bat      # اجرای کامل پروژه ⭐⭐
│   ├── start-full-project.ps1      # نسخه PowerShell
│   └── fix-python-314.bat          # حل مشکل Python 3.14
│
└── ⚙️ فایل‌های تنظیمات
    ├── package.json                # Dependencies Frontend
    ├── next.config.js              # تنظیمات Next.js
    ├── tailwind.config.ts          # تنظیمات Tailwind
    ├── tsconfig.json               # تنظیمات TypeScript
    └── eslint.config.js            # تنظیمات ESLint
```

## 🎯 فایل‌های مهم

### برای اجرای پروژه:
1. **`start-full-project.bat`** ⭐⭐ - دابل کلیک کنید!
2. **`fix-python-314.bat`** - اگر خطای Python دیدید

### برای مطالعه:
1. **`README.md`** ⭐ - راهنمای اصلی
2. **`README_QUICK_START.md`** - راهنمای سریع
3. **`START_PROJECT_FULL.md`** - راهنمای کامل
4. **`INSTALL_PYTHON_313.md`** - نصب Python 3.13
5. **`SOLVE_PYTHON_314.md`** - حل مشکل Python 3.14

---

**ساختار پروژه به‌روزرسانی شده است! 🎉**

