"""Settings loaded from environment variables (and a local .env file)."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")


@dataclass(frozen=True)
class Settings:
    model: str
    effort: str
    max_tokens: int


def get_settings() -> Settings:
    load_dotenv()
    effort = os.getenv("CLAUDE_EFFORT", "high").lower()
    if effort not in EFFORT_LEVELS:
        raise ValueError(f"CLAUDE_EFFORT must be one of {EFFORT_LEVELS}, got {effort!r}")
    return Settings(
        model=os.getenv("CLAUDE_MODEL", "claude-opus-5-5"),
        effort=effort,
        max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "64000")),
    )
