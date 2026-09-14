from __future__ import annotations

from collections.abc import Iterable

from core.message import Message
from core.permission import PermissionVerdict
from protocols.mediator import Context
from protocols.tool import Tool
from services.permission_gate import PermissionGate


class ToolRunner:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._by_name: dict[str, Tool] = {t.name: t for t in tools}
        self._permission_gate = PermissionGate()

    def add(self, tool: Tool) -> None:
        self._by_name[tool.name] = tool

    def run(self, call: dict, ctx: Context) -> Message:
        name = call.get("name", "")
        decision = self._permission_gate.decide(call, ctx)

        if decision.verdict == PermissionVerdict.DENY:
            content = f"denied: {decision.reason or 'not permitted'}"
        else:
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
