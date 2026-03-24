from __future__ import annotations

import os
from typing import Iterable


def _mock_chat(system: str | None, user: str) -> str:
    """
    Deterministic fallback so the demos run without API keys.
    """
    system_part = f"[system: {system.strip()}] " if system else ""

    lowered = user.lower()
    if "plan" in lowered:
        return f"{system_part}Plan (mock): 1) Identify needed info 2) Call tool if useful 3) Draft final answer."
    if "time" in lowered:
        return f"{system_part}Mock answer: It's a demo run, so I won't call external services."
    return f"{system_part}Mock answer: {user}"


def chat_completion(
    *,
    user: str,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.2,
) -> str:
    """
    Returns a single text response.

    If OPENAI_API_KEY is missing, returns a deterministic mock response.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _mock_chat(system, user)

    from openai import OpenAI

    chosen_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    resp = client.chat.completions.create(
        model=chosen_model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


def format_conversation(messages: Iterable[dict]) -> str:
    """Utility for putting a list of messages into a readable string."""
    lines: list[str] = []
    for m in messages:
        role = m.get("role", "unknown")
        content = (m.get("content") or "").strip()
        lines.append(f"{role}: {content}")
    return "\n".join(lines)
