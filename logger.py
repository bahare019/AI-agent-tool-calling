import datetime
import json

from config import LOG_FILE


def log_tool_call(tool_name, args, result):
    """هر بار که یه ابزار اجرا میشه، جزئیاتش رو تو یه فایل متنی ثبت می‌کنه."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}] ابزار: {tool_name}\n"
        f"ورودی: {json.dumps(args, ensure_ascii=False)}\n"
        f"خروجی: {result[:300]}\n"
        f"{'-' * 50}\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
