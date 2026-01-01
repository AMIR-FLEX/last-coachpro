# 🔧 حل مشکل Python 3.14 - راهنمای کامل

## ❌ مشکل
Python 3.14 خیلی جدید است و کتابخانه‌های Rust-based مثل `orjson` و `pydantic-core` هنوز از آن پشتیبانی کامل ندارند.

## ✅ راه‌حل‌های سریع

### 🎯 راه‌حل 1: استفاده از requirements-fix.txt (بدون orjson) - ⚡ سریع‌ترین

**orjson** فقط برای سرعت بیشتر JSON است و در کد استفاده نمی‌شود. می‌توانید بدون آن کار کنید:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements-fix.txt
```

یا:

```bash
.\install-backend-manual.bat
```

### 🎯 راه‌حل 2: نصب Python 3.13 (توصیه می‌شود) - 🏆 بهترین

1. **دانلود Python 3.13**: 
   - لینک: https://www.python.org/downloads/
   - انتخاب: **Python 3.13.x** (نه 3.14)

2. **نصب Python 3.13**:
   - هنگام نصب، حتماً **"Add Python to PATH"** را تیک بزنید

3. **حذف virtual environment قدیمی**:
   ```powershell
   Remove-Item -Recurse -Force backend\venv
   ```

4. **اجرای مجدد**:
   ```powershell
   .\start-full-project.bat
   ```

### 🎯 راه‌حل 3: استفاده از Python 3.11 (بسیار پایدار)

Python 3.11 یکی از پایدارترین نسخه‌هاست و همه کتابخانه‌ها از آن پشتیبانی می‌کنند:

- دانلود: https://www.python.org/downloads/release/python-31112/

## 📋 مراحل دقیق برای نصب Python 3.13

### گام 1: حذف Python 3.14 (اختیاری)

```powershell
# بررسی نسخه فعلی
python --version

# اگر می‌خواهید Python 3.14 را حذف کنید (اختیاری)
# از Control Panel > Programs > Uninstall
```

### گام 2: نصب Python 3.13

1. دانلود از: https://www.python.org/downloads/release/python-3133/
2. اجرای installer
3. **مهم**: تیک "Add Python to PATH" را بزنید
4. Install Now را کلیک کنید

### گام 3: بررسی نصب

```powershell
python --version
# باید بگوید: Python 3.13.x
```

### گام 4: حذف و ساخت مجدد venv

```powershell
cd "C:\Users\amirhossein\Desktop\LAST COACH APP\backend"
Remove-Item -Recurse -Force venv
python -m venv venv
```

### گام 5: نصب Dependencies

```powershell
.\venv\Scripts\Activate.ps1
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

### گام 6: اجرای پروژه

```powershell
cd ..
.\start-full-project.bat
```

## 🔍 بررسی اینکه کدام Python استفاده می‌شود

```powershell
# بررسی نسخه Python
python --version

# بررسی مسیر Python
where python

# بررسی تمام نسخه‌های Python نصب شده
Get-Command python* | Select-Object Source
```

## ⚠️ نکات مهم

1. **PATH Priority**: اگر چند Python نصب دارید، اولی که در PATH است استفاده می‌شود
2. **Virtual Environment**: همیشه از venv استفاده کنید
3. **orjson**: اگر نصب نشد، مشکلی نیست! فقط پروژه کمی کندتر می‌شود
4. **pydantic-core**: برای Pydantic ضروری است، باید نصب شود

## 🆘 اگر هنوز مشکل دارید

### استفاده از requirements-fix.txt:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements-fix.txt
```

این فایل `orjson` ندارد و پروژه بدون آن کار می‌کند.

### بررسی اینکه چه مشکلی دارید:

```powershell
# بررسی خطاهای دقیق
pip install -r requirements.txt -v

# یا فقط یک کتابخانه خاص:
pip install pydantic-core -v
```

## 📞 نسخه‌های پشتیبانی شده

| نسخه Python | وضعیت | توضیحات |
|------------|-------|---------|
| 3.8 | ✅ | قدیمی ولی کار می‌کند |
| 3.9 | ✅ | کار می‌کند |
| 3.10 | ✅ | کار می‌کند |
| 3.11 | ✅✅ | **توصیه می‌شود** - بسیار پایدار |
| 3.12 | ✅ | کار می‌کند |
| 3.13 | ✅✅ | **توصیه می‌شود** - جدید و پایدار |
| 3.14 | ❌ | **مشکل دارد** - خیلی جدید |

## ✨ خلاصه

**بهترین راه**: Python 3.11 یا 3.13 نصب کنید و virtual environment را دوباره بسازید.

**راه سریع**: از `requirements-fix.txt` استفاده کنید (بدون orjson).

---

**موفق باشید! 🚀**

