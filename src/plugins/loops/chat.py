from __future__ import annotations

from core.message import Message
from protocols.loop import Loop
from protocols.mediator import Context
from core.invoke import invoke


class ChatLoop(Loop):

    async def run(self, ctx: Context) -> str:
        history = ctx.history
        for cm in ctx.all("context"):
            history = await invoke(cm.process, history, ctx)
        response = await invoke(ctx.get("provider").complete, history, ctx)
        ctx.add_message(Message(role="assistant", content=response.text))
        return response.text
