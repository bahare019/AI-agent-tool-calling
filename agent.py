import json

from config import client, MODEL
from history import load_history, save_history
from logger import log_tool_call
from tools import tools, available_functions


def run_agent(user_input: str, max_turns: int = 6):
    messages = load_history()
    messages.append({"role": "user", "content": user_input})
    save_history(messages)

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        msg = response.choices[0].message
        messages.append(msg)
        save_history(messages)

        # اگه مدل تصمیم نگرفته ابزاری صدا بزنه، یعنی جواب نهایی آماده‌ست
        if not msg.tool_calls:
            return msg.content

        # مدل یک یا چند ابزار خواسته؛ هرکدوم رو اجرا می‌کنیم
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"\n[ابزار صدا زده شد: {func_name}({func_args})]")

            func = available_functions.get(func_name)
            result = func(**func_args) if func else f"ابزار ناشناخته: {func_name}"
            log_tool_call(func_name, func_args, str(result))

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )
            save_history(messages)

    return "تعداد دورهای مجاز تمام شد؛ جواب نهایی دریافت نشد."


if __name__ == "__main__":
    while True:
        user_input = input("\nشما: ")
        if user_input.lower() in ["exit", "quit", "خروج"]:
            break
        answer = run_agent(user_input)
        print(f"\nایجنت: {answer}")
