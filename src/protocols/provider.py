from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, runtime_checkable

if TYPE_CHECKING:
    from protocols.mediator import Context

# A message is a plain dict: {"role": "user"|"assistant"|"tool", "content": str}.
Message = dict[str, Any]


@dataclass
class Response:
    """
    Response of the provider for one completion
    """

    text: str = ""
    tool_calls: list[dict] = field(default_factory=list)


@runtime_checkable
class Provider(Protocol):
    """
    A model backend.
    """

    kind: ClassVar[str] = "provider"

    @abstractmethod
    def complete(self, history: list[Message], ctx: Context) -> Response: ...
