from __future__ import annotations

from abc import abstractmethod
from collections.abc import Awaitable
from typing import ClassVar, Protocol, runtime_checkable

from protocols.mediator import Context


@runtime_checkable
class Approver(Protocol):
    kind: ClassVar[str] = "approver"

    @abstractmethod
    def approve(
        self, call: dict, reason: str, ctx: Context
    ) -> bool | Awaitable[bool]:
        """
        Approve or deny an asked-for tool call.
        May be sync or ``async def`` — the harness adapts.
        """
