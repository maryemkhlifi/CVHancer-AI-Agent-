"""Interactive streaming chat with Claude. Run: uv run ai-chat"""

import anthropic

from ai_project.client import FALLBACK_BETA, make_client
from ai_project.config import get_settings

SYSTEM_PROMPT = "You are a helpful, concise assistant."


def main() -> None:
    settings = get_settings()
    client = make_client()
    messages: list = []

    print(f"Chatting with {settings.model} (effort={settings.effort}). Type 'exit' to quit.\n")
    while True:
        try:
            user_input = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        print("claude > ", end="", flush=True)
        try:
            with client.beta.messages.stream(
                model=settings.model,
                max_tokens=settings.max_tokens,
                system=SYSTEM_PROMPT,
                output_config={"effort": settings.effort},
                cache_control={"type": "ephemeral"},  # cache the growing conversation
                betas=[FALLBACK_BETA],
                fallbacks="default",
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                response = stream.get_final_message()
        except anthropic.APIError as e:
            print(f"\n[error] {e}\n")
            messages.pop()  # drop the unanswered user turn
            continue
        print("\n")

        if response.stop_reason == "refusal":
            print("[the request was declined]\n")
        # Append the full content (not just the text) so thinking blocks are preserved.
        messages.append({"role": "assistant", "content": response.content})


if __name__ == "__main__":
    main()
