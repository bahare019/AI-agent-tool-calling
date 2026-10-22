import ast
import operator

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
        return ALLOWED_OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError("عبارت نامعتبر")


def calculate(expression: str) -> str:
    """یک عبارت ریاضی ساده را به‌صورت امن محاسبه می‌کند."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_eval_node(tree.body))
    except ZeroDivisionError:
        return "خطا: تقسیم بر صفر"
    except Exception as e:
        return f"خطا در محاسبه: {e}"


SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "یک عبارت ریاضی ساده (جمع، تفریق، ضرب، تقسیم، توان، باقیمانده) را محاسبه می‌کند. برای محاسبات ساده به‌جای run_python_code از این استفاده کن.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "عبارت ریاضی، مثلاً 25 ** 3 + 4 * 2",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]

FUNCTIONS = {"calculate": calculate}
