# 📤 راهنمای کامل بارگذاری و بروزرسانی پروژه در GitHub

## ✅ وضعیت فعلی

Repository از قبل تنظیم شده است:
- **Remote URL**: `https://github.com/AMIR-FLEX/last-coachpro.git`
- **Branch**: `main`

## 🚀 روش‌های بروزرسانی

### روش 1: استفاده از اسکریپت (پیشنهادی)

**برای Windows:**
```bash
push-to-github.bat
```

**برای PowerShell:**
```powershell
.\push-to-github.ps1
```

### روش 2: دستورات دستی

```bash
# 1. اضافه کردن تمام تغییرات
git add .

# 2. Commit تغییرات
git commit -m "توضیحات تغییرات"

# 3. Push به GitHub
git push origin main
```

## 📋 تغییرات انجام شده در این بروزرسانی

### ✨ ویژگی‌های جدید:
- ✅ کامل شدن Migration به Next.js 14
- ✅ تبدیل تمام کامپوننت‌ها به TypeScript
- ✅ اتصال کامل Backend به Frontend
- ✅ رفع تمام باگ‌ها و مشکلات
- ✅ اضافه شدن PostCSS config
- ✅ اصلاح Dependencies

### 🗑️ فایل‌های حذف شده:
- ❌ پوشه `src/` قدیمی (React/Vite)
- ❌ فایل‌های config قدیمی (vite.config.js, tailwind.config.js)
- ❌ فایل‌های batch قدیمی و غیرضروری

### 📁 ساختار جدید:
```
📁 FLEX PRO/
├── app/              # Next.js App Router
├── components/       # TypeScript Components
├── lib/             # API Client & Utils
├── store/           # Zustand Stores
├── types/           # TypeScript Types
├── backend/         # FastAPI Backend
└── ...
```

## 📝 دستورات مفید Git

### بررسی وضعیت:
```bash
git status
git log --oneline -10
```

### Pull تغییرات از GitHub:
```bash
git pull origin main
```

### Reset به آخرین Commit (در صورت نیاز):
```bash
git reset --hard HEAD
```

### مشاهده تفاوت‌ها:
```bash
git diff
```

## 🔒 فایل‌های نادیده گرفته شده (.gitignore)

فایل‌های زیر به GitHub push نمی‌شوند:
- `node_modules/`
- `backend/venv/`
- `.next/`
- `.env`
- `*.db` (Database files)
- `__pycache__/`
- و سایر فایل‌های موقت

## 📖 مستندات

برای راهنمای کامل پروژه:
- `README.md` - راهنمای اصلی
- `PROJECT_STRUCTURE.md` - ساختار پروژه
- `START_PROJECT_FULL.md` - راهنمای اجرا

---

**موفق باشید! 🎉**

