from tools import calculator, code_runner, file_tools, web_search

tools = (
    calculator.SCHEMAS + code_runner.SCHEMAS + file_tools.SCHEMAS + web_search.SCHEMAS
)

# دیکشنری برای صدا زدن تابع واقعی بر اساس اسمی که مدل برمی‌گردونه
available_functions = {
    **calculator.FUNCTIONS,
    **code_runner.FUNCTIONS,
    **file_tools.FUNCTIONS,
    **web_search.FUNCTIONS,
}
