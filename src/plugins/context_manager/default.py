from __future__ import annotations

from protocols.context import ContextManager
from protocols.mediator import Context
from protocols.provider import Message


class DefaultContextManager(ContextManager):
    def process(self, history: list[Message], ctx: Context) -> list[Message]:
        return history
