from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable

from protocols.mediator import Context


@runtime_checkable
class Tool(Protocol):
    kind: ClassVar[str] = "tool"

    name: str
    description: str
    parameters: dict

    @abstractmethod
    def run(self, arguments: dict, ctx: Context) -> str: ...
