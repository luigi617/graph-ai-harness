from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable

from core.message import Message


@runtime_checkable
class Tracer(Protocol):
    kind: ClassVar[str] = "tracer"

    @abstractmethod
    def on_node(self, node: Message) -> None: ...
