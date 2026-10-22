from pathlib import Path
from config import WORKSPACE


def _safe_path(path: str) -> Path:
    full = (WORKSPACE / path.lstrip("/\\")).resolve()
    if not full.is_relative_to(WORKSPACE):
        raise ValueError("مسیر خارج از workspace مجاز نیست")
    return full


def list_files(path: str = ".") -> str:
    """فایل‌ها و پوشه‌های داخل workspace را لیست می‌کند."""
    try:
        folder = _safe_path(path)
        if not folder.is_dir():
            return "خطا: این مسیر پوشه نیست"
        items = sorted(folder.iterdir())
        if not items:
            return "(پوشه خالی است)"
        return "\n".join(
            f"{'[پوشه]' if p.is_dir() else '[فایل]'} {p.relative_to(WORKSPACE)}"
            for p in items
        )
    except Exception as e:
        return f"خطا: {e}"


def read_file(path: str) -> str:
    """محتوای یک فایل داخل workspace را می‌خواند."""
    try:
        return _safe_path(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"خطا در خواندن فایل: {e}"


def write_file(path: str, content: str) -> str:
    """محتوا را در یک فایل داخل workspace می‌نویسد."""
    try:
        full = _safe_path(path)
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        return f"فایل در workspace/{full.relative_to(WORKSPACE)} ذخیره شد."
    except Exception as e:
        return f"خطا در نوشتن فایل: {e}"


SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "فایل‌ها و پوشه‌های داخل workspace را لیست می‌کند. قبل از کار با فایل‌ها (مثلاً تحلیل داده) از این ابزار استفاده کن تا بدانی چه فایل‌هایی موجود است.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "مسیر پوشه نسبت به workspace؛ پیش‌فرض ریشه‌ی workspace",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "محتوای یک فایل را از روی دیسک می‌خواند.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "مسیر فایل"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "محتوا را در یک فایل روی دیسک ذخیره می‌کند.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "مسیر فایل"},
                    "content": {
                        "type": "string",
                        "description": "محتوایی که باید نوشته شود",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]

FUNCTIONS = {"read_file": read_file, "write_file": write_file, "list_files": list_files}
