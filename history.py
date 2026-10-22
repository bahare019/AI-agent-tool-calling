# history.py
import json

from config import HISTORY_FILE, SYSTEM_PROMPT


def load_history():
    """اگه فایل تاریخچه وجود داشته باشه، messages رو از توش می‌خونه؛ وگرنه یه لیست پیش‌فرض می‌سازه."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def save_history(messages):
    """لیست messages رو تو فایل JSON ذخیره می‌کنه."""
    serializable = [m if isinstance(m, dict) else m.model_dump() for m in messages]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)
