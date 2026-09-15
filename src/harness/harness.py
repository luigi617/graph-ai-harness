from __future__ import annotations

import asyncio

from core.events import SessionEnded, SessionStarted
from core.message import Message
from harness.mediator import RunContext
from harness.registry import Registry
from harness.session import Session
from core.invoke import invoke

ENTRY_KIND = "loop"


class GraphAIHarness:
    def __init__(self) -> None:
        self._registry = Registry()

    def use(self, plugin: object) -> "GraphAIHarness":
        self._registry.add(plugin)
        return self

    async def run(self, user_input: str) -> str:
        session = Session()
        ctx = RunContext(session, self._registry)
        loop = self._registry.get(ENTRY_KIND)
        if loop is None:
            raise LookupError(f"no {ENTRY_KIND!r} plugin registered")

        ctx.emit(SessionStarted(session.id))
        ctx.add_message(Message(role="user", content=str(user_input)))
        result = await invoke(loop.run, ctx)
        ctx.emit(SessionEnded(session.id, result))
        return result

    def run_sync(self, user_input: str) -> str:
        """Synchronous entry point."""
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.run(user_input))
        raise RuntimeError(
            "GraphAIHarness.run_sync() cannot be called from a running event "
            "loop; await run() instead."
        )
