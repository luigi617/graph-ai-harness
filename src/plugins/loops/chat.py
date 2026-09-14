from __future__ import annotations

from core.message import Message
from protocols.loop import Loop
from protocols.mediator import Context


class ChatLoop(Loop):

    def run(self, ctx: Context) -> str:
        history = ctx.history
        for cm in ctx.all("context"):  # request middleware chain
            history = cm.process(history, ctx)
        response = ctx.get("provider").complete(history, ctx)
        ctx.add_message(Message(role="assistant", content=response.text))
        return response.text
