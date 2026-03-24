from __future__ import annotations

import datetime as dt
import os
from typing import Any


def get_current_time_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def tavily_search(query: str, *, max_results: int = 3) -> str:
    """
    Searches the web using Tavily if TAVILY_API_KEY is set.
    Otherwise returns a mock string.
    """
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        return f"[mock_search] query={query!r} max_results={max_results} (no TAVILY_API_KEY set)"

    from tavily import TavilyClient

    client = TavilyClient(api_key=api_key)
    res: Any = client.search(query=query, max_results=max_results)

    if isinstance(res, dict):
        results = res.get("results") or []
    else:
        results = []

    lines: list[str] = [f"[tavily_search] query={query!r}"]
    for r in results[:max_results]:
        title = (r.get("title") or "").strip()
        url = (r.get("url") or "").strip()
        snippet = (r.get("content") or r.get("snippet") or "").strip()
        lines.append(f"- {title} ({url}) {snippet}".strip())
    return "\n".join(lines).strip()
