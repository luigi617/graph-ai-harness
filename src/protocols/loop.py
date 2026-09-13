from __future__ import annotations

from abc import abstractmethod
from typing import ClassVar, Protocol, runtime_checkable

from protocols.mediator import Context


@runtime_checkable
class Loop(Protocol):
    """
    A loop plugin. Drives a Session to completion and returns final text.
    """

    kind: ClassVar[str] = "loop"

    @abstractmethod
    def run(self, ctx: Context) -> str: ...
