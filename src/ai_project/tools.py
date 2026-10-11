"""Tools the agent can call. Each wraps a plain, testable function."""

import ast
import operator
from datetime import datetime, timezone

from anthropic import beta_tool

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_eval(expression: str) -> float:
    """Evaluate a pure arithmetic expression without using eval()."""

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
            right = _eval(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("exponent too large")
            return _BIN_OPS[type(node.op)](_eval(node.left), right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
            return _UNARY_OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"unsupported expression: {type(node).__name__}")

    return _eval(ast.parse(expression, mode="eval"))


@beta_tool
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression exactly. Use this instead of doing math in your head.

    Args:
        expression: Arithmetic using + - * / // % ** and parentheses, e.g. "(3 + 4) * 2".
    """
    try:
        return str(safe_eval(expression))
    except (ValueError, SyntaxError, ZeroDivisionError) as e:
        return f"Error: {e}"


@beta_tool
def current_time() -> str:
    """Get the current date and time in UTC (ISO 8601)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


ALL_TOOLS = [calculate, current_time]
