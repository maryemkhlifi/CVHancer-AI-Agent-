"""Shared Anthropic client and request defaults."""

import anthropic

# On a safety-classifier refusal, the API re-runs the request on a suitable fallback
# model inside the same call. fallbacks="default" routes by refusal category.
FALLBACK_BETA = "server-side-fallback-2026-07-01"


def make_client() -> anthropic.Anthropic:
    # Resolves credentials from ANTHROPIC_API_KEY or an `ant auth login` profile.
    return anthropic.Anthropic()
