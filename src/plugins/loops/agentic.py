from __future__ import annotations

from core.message import Message
from plugins.tools import ToolRunner
from protocols.loop import Loop
from protocols.mediator import Context


class AgenticLoop(Loop):

    def __init__(self, max_iters: int = 25) -> None:
        self.max_iters = max_iters

    def run(self, ctx: Context) -> str:
        provider = ctx.get("provider")
        tools = ToolRunner(ctx.all("tool"))
        for _ in range(self.max_iters):
            if ctx.interrupted:  # control
                return "stopped: interrupted"

            history = ctx.history
            for cm in ctx.all("context"):  # middleware chain
                history = cm.process(history, ctx)
            response = provider.complete(history, ctx)
            ctx.add_message(
                Message(
                    role="assistant",
                    content=response.text,
                    tool_calls=response.tool_calls,
                )
            )

            if not response.tool_calls:  # natural exit
                return response.text

            for call in response.tool_calls:
                ctx.add_message(tools.run(call, ctx))

        return "stopped: reached max_iters guard"  # guard exit
