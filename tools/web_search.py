from ddgs import DDGS


def search_web(query: str) -> str:
    """تو وب جست‌وجو می‌کنه و چند نتیجه‌ی اول رو برمی‌گردونه."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "هیچ نتیجه‌ای پیدا نشد."

        formatted = []
        for r in results:
            formatted.append(
                f"عنوان: {r['title']}\nلینک: {r['href']}\nخلاصه: {r['body']}"
            )
        return "\n\n".join(formatted)
    except Exception as e:
        return f"خطا در جست‌وجو: {str(e)}"


SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "در اینترنت جست‌وجو می‌کند و نتایج مرتبط را برمی‌گرداند. برای سؤالاتی که نیاز به اطلاعات به‌روز یا خارج از دانش مدل دارند استفاده کن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "عبارت جست‌وجو"}
                },
                "required": ["query"],
            },
        },
    },
]

FUNCTIONS = {
    "search_web": search_web,
}
