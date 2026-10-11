# CLAUDE.md

Python AI project on the Anthropic SDK, managed with uv. Source lives in `src/ai_project/`.

## Commands
- Install: `uv sync`
- Test: `uv run pytest` (tests must not call the API)
- Lint/format: `uv run ruff check .` / `uv run ruff format .`
- Run: `uv run ai-chat`, `uv run ai-agent "<task>"`

## Conventions
- Default model is `claude-opus-5-5`, read from `config.get_settings()`. Never hardcode model IDs elsewhere.
- Use the official `anthropic` SDK. No raw HTTP calls.
- Streaming for long outputs. When continuing a conversation, append the full `response.content`, not just the text.
- Thinking can't be disabled on Opus 5.5. Control depth with `output_config={"effort": ...}`.
- New agent tools go in `tools.py`: put the logic in a plain function with unit tests, then wrap it with `@beta_tool`.
- Secrets live only in `.env`, which is gitignored.
