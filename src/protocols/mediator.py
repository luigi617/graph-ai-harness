from __future__ import annotations

from typing import Protocol, runtime_checkable

from protocols.provider import Message


@runtime_checkable
class Context(Protocol):
    history: list[Message]
    interrupted: bool

    def get(self, kind: str) -> object | None: ...

    def all(self, kind: str) -> list[object]: ...
