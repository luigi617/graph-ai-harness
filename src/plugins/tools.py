from __future__ import annotations

from collections.abc import Iterable

from core.message import Message
from protocols.mediator import Context
from protocols.tool import Tool


class ToolRunner:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._by_name: dict[str, Tool] = {t.name: t for t in tools}

    def add(self, tool: Tool) -> None:
        self._by_name[tool.name] = tool

    def run(self, call: dict, ctx: Context) -> Message:
        name = call.get("name", "")
        tool = self._by_name.get(name)
        if tool is None:
            content = f"error: unknown tool {name!r}"
        else:
            content = tool.run(call.get("arguments", {}), ctx)
        return Message(
            role="tool",
            content=content,
            name=name,
            tool_use_id=call.get("id"),
        )
