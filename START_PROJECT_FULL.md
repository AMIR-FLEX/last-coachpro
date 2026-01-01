# 🚀 راهنمای اجرای کامل پروژه FLEX PRO

این راهنما برای اجرای همزمان Backend و Frontend پروژه است.

## 📋 پیش‌نیازها

1. **Python 3.8+** - [دانلود Python](https://www.python.org/downloads/)
2. **Node.js 18+** - [دانلود Node.js](https://nodejs.org/)
3. **Git** (اختیاری)

## 🎯 روش اجرا (ساده‌ترین روش)

### روش 1: استفاده از فایل Batch (پیشنهادی برای Windows)

1. روی فایل `start-full-project.bat` دابل کلیک کنید
2. صبر کنید تا پروژه راه‌اندازی شود
3. دو پنجره CMD باز می‌شود:
   - **FLEX PRO - Backend** (پورت 8000)
   - **FLEX PRO - Frontend** (پورت 3000)

### روش 2: استفاده از PowerShell

1. PowerShell را به عنوان Administrator اجرا کنید
2. دستور زیر را اجرا کنید:
   ```powershell
   .\start-full-project.ps1
   ```

### روش 3: اجرای دستی (برای توسعه‌دهندگان)

#### 1️⃣ راه‌اندازی Backend

```bash
# رفتن به پوشه Backend
cd backend

# فعال‌سازی Virtual Environment
.\venv\Scripts\Activate.ps1    # PowerShell
# یا
.\venv\Scripts\activate.bat    # CMD

# نصب Dependencies (در صورت نیاز)
pip install -r requirements.txt

# اجرای Backend
python run.py
```

Backend در آدرس زیر در دسترس است:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

#### 2️⃣ راه‌اندازی Frontend

```bash
# بازگشت به پوشه اصلی
cd ..

# کپی کردن package-nextjs.json به package.json (در صورت نیاز)
copy package-nextjs.json package.json

# نصب Dependencies (در صورت نیاز)
npm install

# اجرای Frontend
npm run dev
```

Frontend در آدرس زیر در دسترس است:
- **Frontend**: http://localhost:3000

## 📍 آدرس‌های مهم

پس از اجرای پروژه، به آدرس‌های زیر دسترسی دارید:

- **Frontend (Next.js)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

## ⚙️ تنظیمات

### Backend

فایل تنظیمات: `backend/app/config.py`

- **Database**: SQLite (پیش‌فرض: `flexpro.db`)
- **Port**: 8000
- **Host**: 0.0.0.0

### Frontend

فایل تنظیمات: `next.config.js`

- **Port**: 3000 (پیش‌فرض Next.js)
- **API URL**: از `lib/api-client.ts` تنظیم می‌شود

## 🔧 عیب‌یابی

### مشکل: Python پیدا نشد
**راه‌حل**: Python را نصب کنید و PATH را به‌روزرسانی کنید.

### مشکل: Node.js پیدا نشد
**راه‌حل**: Node.js را نصب کنید و PATH را به‌روزرسانی کنید.

### مشکل: Virtual Environment کار نمی‌کند
**راه‌حل**:
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### مشکل: Dependencies نصب نمی‌شوند
**راه‌حل**:
```bash
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
npm cache clean --force
npm install
```

### مشکل: پورت 8000 یا 3000 اشغال است
**راه‌حل**: 
1. برنامه دیگری که از این پورت‌ها استفاده می‌کند را ببندید
2. یا در `backend/run.py` و `next.config.js` پورت را تغییر دهید

### مشکل: دیتابیس ایجاد نمی‌شود
**راه‌حل**:
```bash
cd backend
.\venv\Scripts\Activate.ps1
python -c "from app.db.init_db import init_db; init_db()"
```

## 🛑 توقف پروژه

برای توقف پروژه:
- پنجره‌های CMD/PowerShell را ببندید
- یا `Ctrl+C` را در هر پنجره بزنید

## 📝 یادداشت‌ها

- اولین بار اجرا ممکن است کمی طول بکشد (نصب dependencies)
- Backend باید قبل از Frontend اجرا شود
- برای تغییرات در Backend، سرور به صورت خودکار reload می‌شود
- برای تغییرات در Frontend، Next.js به صورت خودکار Hot Reload می‌کند

## 🔗 لینک‌های مفید

- [مستندات FastAPI](https://fastapi.tiangolo.com/)
- [مستندات Next.js](https://nextjs.org/docs)
- [مستندات React Query](https://tanstack.com/query/latest)

---

**موفق باشید! 🎉**

