from __future__ import annotations

from core.events import IterationStarted, LoopStopped, ResponseReceived
from core.message import Message
from protocols.loop import Loop
from protocols.mediator import Context
from services.guard_chain import GuardChain
from services.tool_runner import ToolRunner


class AgenticLoop(Loop):

    def run(self, ctx: Context) -> str:
        provider = ctx.get("provider")
        tools = ToolRunner(ctx.all("tool"))
        guards = GuardChain()

        i = 0
        while True:
            if ctx.interrupted:  # control
                ctx.emit(LoopStopped("interrupted"))
                return "stopped: interrupted"

            ctx.emit(IterationStarted(i))
            decision = guards.check(ctx)
            if decision.stop:
                ctx.emit(LoopStopped(f"guard: {decision.reason}"))
                return f"stopped: {decision.reason}"

            history = ctx.history
            for cm in ctx.all("context"):  # middleware chain
                history = cm.process(history, ctx)
            response = provider.complete(history, ctx)
            ctx.emit(ResponseReceived(response))
            ctx.add_message(
                Message(
                    role="assistant",
                    content=response.text,
                    tool_calls=response.tool_calls,
                )
            )

            if not response.tool_calls:  # natural exit — model is done
                ctx.emit(LoopStopped("completed"))
                return response.text

            for call in response.tool_calls:
                ctx.add_message(tools.run(call, ctx))
            i += 1
