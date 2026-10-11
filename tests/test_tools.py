import pytest

from ai_project.config import get_settings
from ai_project.tools import safe_eval


@pytest.mark.parametrize(
    ("expr", "expected"),
    [("1 + 2", 3), ("(3 + 4) * 2", 14), ("2 ** 10", 1024), ("-5 + 10 / 4", -2.5), ("7 // 2", 3)],
)
def test_safe_eval(expr, expected):
    assert safe_eval(expr) == expected


@pytest.mark.parametrize("expr", ["__import__('os')", "a + 1", "2 ** 100000", "[1, 2]"])
def test_safe_eval_rejects_unsafe(expr):
    with pytest.raises(ValueError):
        safe_eval(expr)


def test_settings_defaults(monkeypatch):
    monkeypatch.setattr("ai_project.config.load_dotenv", lambda: None)
    for var in ("CLAUDE_MODEL", "CLAUDE_EFFORT", "CLAUDE_MAX_TOKENS"):
        monkeypatch.delenv(var, raising=False)
    s = get_settings()
    assert s.model == "claude-opus-5-5"
    assert s.effort == "high"
    assert s.max_tokens == 64000


def test_settings_rejects_bad_effort(monkeypatch):
    monkeypatch.setattr("ai_project.config.load_dotenv", lambda: None)
    monkeypatch.setenv("CLAUDE_EFFORT", "turbo")
    with pytest.raises(ValueError):
        get_settings()
