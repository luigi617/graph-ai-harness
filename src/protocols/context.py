from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable

from core.message import Message
from protocols.mediator import Context


@runtime_checkable
class ContextManager(Protocol):
    """
    Owns everything about managing the context sent to the model
    """

    kind: ClassVar[str] = "context"

    @abstractmethod
    def process(self, history: list[Message], ctx: Context) -> list[Message]: ...
