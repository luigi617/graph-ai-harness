from __future__ import annotations

from core.message import Message
from protocols.context import ContextManager
from protocols.mediator import Context


class DefaultContextManager(ContextManager):
    def process(self, history: list[Message], ctx: Context) -> list[Message]:
        return history
