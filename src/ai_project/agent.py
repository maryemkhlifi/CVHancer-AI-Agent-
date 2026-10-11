"""A tool-using agent: Claude decides when to call the tools in tools.py.

Run: uv run ai-agent "What is 17% of 2340, and what time is it?"
"""

import sys

from ai_project.client import make_client
from ai_project.config import get_settings
from ai_project.tools import ALL_TOOLS

SYSTEM_PROMPT = "You are a precise assistant. Use the available tools whenever they help."


def run(task: str) -> str:
    settings = get_settings()
    client = make_client()

    # The SDK's tool runner drives the request -> tool call -> result loop.
    runner = client.beta.messages.tool_runner(
        model=settings.model,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        output_config={"effort": settings.effort},
        tools=ALL_TOOLS,
        messages=[{"role": "user", "content": task}],
    )

    final = None
    for message in runner:
        final = message
        for block in message.content:
            if block.type == "tool_use":
                print(f"  -> {block.name}({block.input})", file=sys.stderr)

    if final is None:
        return ""
    if final.stop_reason == "refusal":
        return "[the request was declined]"
    return "".join(b.text for b in final.content if b.type == "text")


def main() -> None:
    task = " ".join(sys.argv[1:]) or input("task > ")
    print(run(task))


if __name__ == "__main__":
    main()
