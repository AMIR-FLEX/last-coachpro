# 📥 راهنمای نصب Python 3.13

## چرا Python 3.13؟

Python 3.14 هنوز خیلی جدید است و کتابخانه‌های Rust-based مثل `pydantic-core` و `orjson` از آن پشتیبانی نمی‌کنند.

Python 3.13 پایدار است و همه کتابخانه‌ها از آن پشتیبانی می‌کنند.

## 📋 مراحل نصب

### گام 1: دانلود Python 3.13

1. بروید به: https://www.python.org/downloads/release/python-3133/
2. فایل **Windows installer (64-bit)** را دانلود کنید
3. نام فایل: `python-3.13.3-amd64.exe`

### گام 2: نصب

1. فایل دانلود شده را اجرا کنید
2. **⚠️ مهم**: تیک **"Add Python 3.13 to PATH"** را بزنید
3. روی **"Install Now"** کلیک کنید
4. صبر کنید تا نصب تمام شود

### گام 3: بررسی نصب

PowerShell یا CMD را باز کنید و بزنید:

```powershell
python --version
```

باید بگوید: **Python 3.13.3** (یا نسخه 3.13.x)

### گام 4: حذف Virtual Environment قدیمی

```powershell
cd "C:\Users\amirhossein\Desktop\LAST COACH APP\backend"
Remove-Item -Recurse -Force venv
```

### گام 5: ساخت Virtual Environment جدید

```powershell
python -m venv venv
```

### گام 6: نصب Dependencies

```powershell
.\venv\Scripts\Activate.ps1
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

### گام 7: اجرای پروژه

```powershell
cd ..
.\start-full-project.bat
```

## ✅ بررسی موفقیت

پس از نصب، این دستورات را اجرا کنید:

```powershell
python --version
# باید بگوید: Python 3.13.x

cd backend
.\venv\Scripts\Activate.ps1
pip list | findstr pydantic
# باید pydantic و pydantic-core را ببینید
```

## 🔍 اگر چند Python نصب دارید

اگر چند نسخه Python نصب دارید، می‌توانید از `py` launcher استفاده کنید:

```powershell
# لیست همه Python ها
py --list

# استفاده از Python 3.13 برای venv
py -3.13 -m venv venv
```

## 🆘 مشکلات احتمالی

### مشکل: "python is not recognized"

**راه‌حل**: PATH را بررسی کنید:
1. Windows Settings > System > About > Advanced system settings
2. Environment Variables
3. در System variables، Path را پیدا کنید
4. مطمئن شوید که مسیر Python 3.13 اضافه شده

### مشکل: هنوز Python 3.14 استفاده می‌شود

**راه‌حل**: 
```powershell
# بررسی مسیر Python
where python

# اگر مسیر Python 3.14 است، از py launcher استفاده کنید:
py -3.13 -m venv venv
```

---

**پس از نصب Python 3.13، پروژه بدون مشکل اجرا می‌شود! 🎉**

