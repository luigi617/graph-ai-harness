from __future__ import annotations

from core.events import SessionEnded, SessionStarted
from core.message import Message
from harness.mediator import RunContext
from harness.registry import Registry
from harness.session import Session

ENTRY_KIND = "loop"


class GraphAIHarness:
    def __init__(self) -> None:
        self._registry = Registry()

    def use(self, plugin: object) -> "GraphAIHarness":
        self._registry.add(plugin)
        return self

    def run(self, user_input: str) -> str:
        session = Session()
        ctx = RunContext(session, self._registry)
        loop = self._registry.get(ENTRY_KIND)
        if loop is None:
            raise LookupError(f"no {ENTRY_KIND!r} plugin registered")

        ctx.emit(SessionStarted(session.id))
        ctx.add_message(Message(role="user", content=str(user_input)))
        result = loop.run(ctx)
        ctx.emit(SessionEnded(session.id, result))
        return result
