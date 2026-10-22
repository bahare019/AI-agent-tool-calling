# AI Agent با Tool Calling

یک ایجنت ساده که با OpenRouter کار می‌کند و ابزارهای زیر را دارد:
اجرای کد پایتون (داخل sandbox داکر)، خواندن/نوشتن فایل، جست‌وجوی وب و ماشین‌حساب.

## راه‌اندازی

1. `pip install -r requirements.txt`
2. فایل `.env.example` را کپی کنید به `.env` و کلید OpenRouter را بگذارید
3. ساخت ایمیج sandbox: `docker build -t agent-sandbox:latest sandbox`
4. اجرا: `python agent.py`

## امنیت

کد پایتون مدل داخل یک container بدون اینترنت و با فایل‌سیستم فقط‌خواندنی اجرا می‌شود.
ابزارهای فایل فقط داخل پوشه‌ی `workspace` کار می‌کنند.
