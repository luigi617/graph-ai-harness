from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

from core.events import Event
from core.message import Message

T = TypeVar("T")


@runtime_checkable
class Context(Protocol):
    session_id: str
    history: list[Message]
    interrupted: bool

    @abstractmethod
    def state(self, cls: type[T]) -> T: ...

    @abstractmethod
    def add_message(self, message: Message) -> None: ...

    @abstractmethod
    def emit(self, event: Event) -> None: ...

    @abstractmethod
    def get(self, kind: str) -> object | None: ...

    @abstractmethod
    def all(self, kind: str) -> list[object]: ...
