from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.message import Message


@runtime_checkable
class Context(Protocol):
    session_id: str
    history: list[Message]
    interrupted: bool

    def add_message(self, message: Message) -> None: ...

    def get(self, kind: str) -> object | None: ...

    def all(self, kind: str) -> list[object]: ...
