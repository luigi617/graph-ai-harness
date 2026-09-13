from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable

from protocols.mediator import Context
from protocols.provider import Message


@runtime_checkable
class ContextManager(Protocol):
    """
    Owns everything about managing the context sent to the model
    """

    kind: ClassVar[str] = "context"

    @abstractmethod
    def process(self, history: list[Message], ctx: Context) -> list[Message]: ...
