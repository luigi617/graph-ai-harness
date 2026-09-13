from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable

from core.message import Message
from core.response import Response
from protocols.mediator import Context


@runtime_checkable
class Provider(Protocol):
    """
    A model backend.
    """

    kind: ClassVar[str] = "provider"

    @abstractmethod
    def complete(self, history: list[Message], ctx: Context) -> Response: ...
