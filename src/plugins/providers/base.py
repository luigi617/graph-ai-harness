from __future__ import annotations

from abc import abstractmethod

from protocols.mediator import Context
from protocols.provider import Message, Provider, Response
from protocols.tool import Tool


class BaseProvider(Provider):
    def __init__(self, model: str, **params) -> None:
        self.model = model
        self.params = params

    def complete(self, history: list[Message], ctx: Context) -> Response:
        tools = ctx.all("tool")
        return self._generate(history, tools)

    @abstractmethod
    def _generate(self, history: list[Message], tools: list[Tool]) -> Response: ...
