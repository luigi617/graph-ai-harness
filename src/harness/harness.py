from __future__ import annotations

import asyncio

from harness.mediator import RunContext
from harness.registry import Registry
from harness.session import Session
from services.runner import run_session


class GraphAIHarness:
    def __init__(self) -> None:
        self._registry = Registry()

    def use(self, plugin: object) -> GraphAIHarness:
        self._registry.add(plugin)
        return self

    async def run(self, user_input: str) -> str:
        ctx = RunContext(Session(), self._registry)
        return await run_session(ctx, user_input)

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
