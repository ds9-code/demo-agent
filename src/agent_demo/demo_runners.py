from __future__ import annotations

import asyncio
import os
from typing import Any

from src.agent_demo.llm import chat_completion
from src.agent_demo.tools import get_current_time_iso, tavily_search


def run_custom_orchestrator(user_input: str) -> str:
    """Minimal orchestration without any framework."""

    async def worker() -> dict[str, Any]:
        lowered = user_input.lower()
        needs_tool = any(k in lowered for k in ["search", "weather", "news", "langgraph"])
        tool_result: str | None = None
        trace: list[str] = ["worker:start"]

        if needs_tool:
            trace.append("worker:tool_call")
            if "time" in lowered:
                tool_result = f"[time_tool] {get_current_time_iso()}"
            else:
                tool_result = tavily_search(user_input, max_results=2)
        else:
            trace.append("worker:no_tool")

        trace.append("worker:compose")
        answer = chat_completion(
            system="You are a helpful assistant. Be concise.",
            user=f"User asked: {user_input}\nTool result:\n{tool_result}\n\nWrite the final answer:",
        )
        return {"trace": trace, "answer": answer}

    out = asyncio.run(worker())
    return f"{out['answer']}\n\n[trace] {out['trace']}"


def run_langgraph_demo(user_input: str) -> str:
    """LangGraph: conditional state machine with router, tool, and respond nodes."""
    from typing import TypedDict

    from langgraph.graph import END, StateGraph

    class State(TypedDict):
        user_input: str
        needs_tool: bool
        tool_result: str | None
        answer: str | None
        trace: list[str]

    def router_node(state: State) -> dict[str, Any]:
        trace = state["trace"] + ["router"]
        lowered = state["user_input"].lower()
        needs_tool = any(
            k in lowered for k in ["search", "weather", "news", "langgraph", "tavily", "web"]
        )
        return {"needs_tool": needs_tool, "trace": trace}

    def tool_node(state: State) -> dict[str, Any]:
        trace = state["trace"] + ["tool"]
        lowered = state["user_input"].lower()
        if "time" in lowered:
            tool_result = f"[time_tool] {get_current_time_iso()}"
        else:
            tool_result = tavily_search(state["user_input"], max_results=3)
        return {"tool_result": tool_result, "trace": trace}

    def respond_node(state: State) -> dict[str, Any]:
        trace = state["trace"] + ["respond"]
        answer = chat_completion(
            system="You are a helpful assistant. Use the tool result if present.",
            user=(
                f"User asked: {state['user_input']}\n"
                f"Tool result:\n{state.get('tool_result')}\n\n"
                "Write a final answer in 3-6 sentences:"
            ),
        )
        return {"answer": answer, "trace": trace}

    graph = StateGraph(State)
    graph.add_node("router", router_node)
    graph.add_node("tool", tool_node)
    graph.add_node("respond", respond_node)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        lambda s: "tool" if s["needs_tool"] else "respond",
        {"tool": "tool", "respond": "respond"},
    )
    graph.add_edge("tool", "respond")
    graph.add_edge("respond", END)

    app = graph.compile()
    initial: State = {
        "user_input": user_input,
        "needs_tool": False,
        "tool_result": None,
        "answer": None,
        "trace": [],
    }
    out = app.invoke(initial)
    return f"{out['answer']}\n\n[trace] {out['trace']}"


def run_langchain_demo(user_input: str) -> str:
    """LangChain: LCEL router + branch with RunnableBranch."""
    from langchain_core.runnables import RunnableBranch, RunnableLambda

    def route(x: str) -> dict[str, Any]:
        lowered = x.lower()
        needs_tool = any(
            k in lowered for k in ["search", "weather", "news", "langgraph", "web", "tavily", "time"]
        )
        return {"user_input": x, "needs_tool": needs_tool}

    def do_tool(d: dict[str, Any]) -> dict[str, Any]:
        lowered = d["user_input"].lower()
        if "time" in lowered:
            tool_result = f"[time_tool] {get_current_time_iso()}"
        else:
            tool_result = tavily_search(d["user_input"], max_results=2)
        return {**d, "tool_result": tool_result}

    def skip_tool(d: dict[str, Any]) -> dict[str, Any]:
        return {**d, "tool_result": None}

    def synth(d: dict[str, Any]) -> str:
        return chat_completion(
            system="You are a helpful assistant. Be concise.",
            user=(
                f"User asked: {d['user_input']}\n"
                f"Tool result:\n{d.get('tool_result')}\n\n"
                "Write the final answer:"
            ),
        )

    branch = RunnableBranch(
        (lambda d: bool(d["needs_tool"]), RunnableLambda(do_tool)),
        RunnableLambda(skip_tool),
    )
    chain = RunnableLambda(route) | branch | RunnableLambda(synth)
    answer = chain.invoke(user_input)
    return str(answer)


def run_pyautogen_demo(user_input: str) -> str:
    """pyautogen: multi-agent chat. Requires OPENAI_API_KEY."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return (
            "pyautogen demo (not executed): set OPENAI_API_KEY to run the multi-agent chat.\n"
            "This repo keeps examples safe to run offline by default."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        import autogen
    except Exception as e:
        return f"pyautogen import failed: {e}"

    config_list = [{"model": model, "api_key": api_key}]

    try:
        AssistantAgent = getattr(autogen, "AssistantAgent")
        UserProxyAgent = getattr(autogen, "UserProxyAgent")
    except AttributeError:
        return (
            "pyautogen API mismatch for your installed version.\n"
            "Open examples or update the code to match your autogen package version."
        )

    assistant = AssistantAgent(
        name="assistant",
        llm_config={"config_list": config_list},
    )
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    user_proxy.initiate_chat(
        assistant,
        message=f"Task: {user_input}\n\nPlease respond with a short, structured answer.",
    )

    return "pyautogen demo executed. Check stdout for the conversation transcript."


def pick_demo(demo: str, user_input: str) -> str:
    demo = demo.lower().strip()
    if demo in {"langgraph", "lg"}:
        return run_langgraph_demo(user_input)
    if demo in {"langchain", "lc"}:
        return run_langchain_demo(user_input)
    if demo in {"pyautogen", "autogen"}:
        return run_pyautogen_demo(user_input)
    if demo in {"custom", "plain"}:
        return run_custom_orchestrator(user_input)
    raise ValueError(f"Unknown demo: {demo!r}")
