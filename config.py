import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

MODEL = "openrouter/free"
SANDBOX_IMAGE = "agent-sandbox:latest"

WORKSPACE = (BASE_DIR / "workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)

HISTORY_FILE = BASE_DIR / "history.json"
LOG_FILE = BASE_DIR / "agent_log.txt"

SYSTEM_PROMPT = "تو یک دستیار هوشمند هستی که می‌توانی کد پایتون اجرا کنی و فایل بخوانی/بنویسی و جست و جو از طریق وب انجام بدی. وقتی لازم است، از ابزارها استفاده کن.در sandbox علاوه بر کتابخانه‌های استاندارد پایتون، pandas و numpy نصب است. اینترنت ندارد و فایل‌های workspace فقط‌خواندنی هستند.هرگز داده‌ی ساختگی یا نمونه نساز. اگر کاربر از فایلی نام می‌برد، اول با list_files ببین وجود دارد، سپس آن را مستقیم بخوان. فایل‌های workspace داخل sandbox فقط‌خواندنی‌اند و کد پایتون نباید سعی کند فایل بسازد یا بنویسد. اگر فایل پیدا نشد یا خطا گرفتی، همان را به کاربر بگو و نتیجه‌ی ساختگی نده."
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
