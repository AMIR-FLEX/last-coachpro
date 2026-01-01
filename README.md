# 🏋️ FLEX PRO - سیستم هوشمند مدیریت مربیگری ورزشی

سیستم کامل مدیریت شاگردان، برنامه‌های تمرینی، تغذیه و مکمل‌ها

## 🚀 اجرای سریع

**فقط روی این فایل دابل کلیک کنید:**
```
start-full-project.bat
```

## ⚠️ اگر Python 3.14 دارید

اگر خطای نصب dependencies دیدید:
- **روی این فایل دابل کلیک کنید:** `fix-python-314.bat`
- **یا Python 3.13 نصب کنید:** راهنمای کامل در `INSTALL_PYTHON_313.md`

## 📍 آدرس‌ها پس از اجرا

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🏗️ ساختار پروژه

```
📁 LAST COACH APP/
├── 📁 app/                    # Next.js App Router
│   ├── dashboard/            # صفحات داشبورد
│   ├── login/                # صفحه ورود
│   └── layout.tsx            # Layout اصلی
│
├── 📁 components/            # کامپوننت‌های TypeScript
│   ├── user-list.tsx        # لیست شاگردان
│   ├── user-modal.tsx       # فرم ایجاد/ویرایش شاگرد
│   ├── training-panel.tsx   # برنامه تمرینی
│   ├── diet-panel.tsx       # برنامه تغذیه
│   ├── supplements-panel.tsx # برنامه مکمل
│   └── ...
│
├── 📁 data/                  # داده‌های تمرینات و غذاها
│   ├── resistanceExercises.ts
│   ├── cardioExercises.ts
│   ├── foodData.ts
│   └── ...
│
├── 📁 lib/                   # کتابخانه‌ها
│   ├── api-client.ts        # API Client
│   └── utils.ts             # توابع کمکی
│
├── 📁 store/                 # Zustand Stores
│   ├── app-store.ts         # State مدیریت
│   └── auth-store.ts        # State احراز هویت
│
├── 📁 types/                 # TypeScript Types
│   └── index.ts
│
├── 📁 backend/               # Backend (FastAPI)
│   ├── app/                 # کد اصلی Backend
│   ├── requirements.txt     # Dependencies
│   └── run.py              # اجرای سرور
│
└── 📄 start-full-project.bat # فایل اجرای پروژه ⭐
```

## 🛠️ تکنولوژی‌ها

### Frontend
- **Next.js 14** - Framework
- **TypeScript** - Type Safety
- **React 18** - UI Library
- **Tailwind CSS** - Styling
- **Zustand** - State Management
- **React Query** - Data Fetching
- **Chart.js** - نمودارها
- **Framer Motion** - انیمیشن‌ها

### Backend
- **FastAPI** - Web Framework
- **SQLAlchemy** - ORM
- **SQLite** - Database (Development)
- **JWT** - Authentication
- **Pydantic** - Data Validation

## 📚 راهنماهای کامل

- `START_PROJECT_FULL.md` - راهنمای کامل اجرای پروژه
- `INSTALL_PYTHON_313.md` - راهنمای نصب Python 3.13
- `SOLVE_PYTHON_314.md` - حل مشکل Python 3.14
- `README_QUICK_START.md` - راهنمای سریع

## 🔧 اسکریپت‌های مفید

- `start-full-project.bat` - اجرای کامل پروژه ⭐
- `fix-python-314.bat` - حل مشکل Python 3.14
- `start-full-project.ps1` - نسخه PowerShell

## 💡 نکات مهم

1. **Python 3.11 یا 3.13** توصیه می‌شود (نه 3.14)
2. **Node.js 18+** نیاز است
3. Backend باید روی پورت 8000 اجرا شود
4. Frontend باید روی پورت 3000 اجرا شود

## 📝 دستورات مفید

```bash
# نصب Dependencies Frontend
npm install

# نصب Dependencies Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# اجرای Backend
python run.py

# اجرای Frontend
npm run dev
```

## 📖 مستندات

- **API Documentation**: http://localhost:8000/docs
- **Backend README**: `backend/README.md`

---

**موفق باشید! 💪**
