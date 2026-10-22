import subprocess
import uuid
from config import SANDBOX_IMAGE, WORKSPACE


def run_python_code(code: str) -> str:
    """کد پایتون را داخل یک container ایزوله اجرا می‌کند."""
    container_name = f"agent-sandbox-{uuid.uuid4().hex[:8]}"

    cmd = [
        "docker",
        "run",
        "--rm",
        "--name",
        container_name,
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "0.5",
        "--pids-limit",
        "64",
        "--read-only",
        "--tmpfs",
        "/tmp",
        "--mount",
        f"type=bind,source={WORKSPACE},target=/workspace,readonly",
        "--workdir",
        "/workspace",
        "-e",
        "PYTHONIOENCODING=utf-8",
        SANDBOX_IMAGE,
        "python",
        "-c",
        code,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", timeout=15
        )

        if result.returncode == 137:
            return "خطا: حافظه‌ی sandbox تمام شد (سقف ۲۵۶ مگابایت)"

        output = result.stdout or result.stderr
        return output.strip() or "(کد اجرا شد، خروجی‌ای نداشت)"
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        return "خطا: اجرای کد بیش از حد طول کشید"
    except FileNotFoundError:
        return "خطا: Docker پیدا نشد؛ Docker Desktop باید نصب و روشن باشد."
    except Exception as e:
        return f"خطا: {e}"


SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "کد پایتون را اجرا می‌کند و خروجی آن را برمی‌گرداند. برای محاسبات یا پردازش داده استفاده کن فایل‌های workspace در دسترس است.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "کد پایتون برای اجرا"}
                },
                "required": ["code"],
            },
        },
    },
]

FUNCTIONS = {
    "run_python_code": run_python_code,
}
