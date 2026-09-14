from __future__ import annotations

from typing import TypeVar

from core.events import Event, MessageAdded
from core.message import Message
from harness.registry import Registry
from harness.session import Session
from protocols.mediator import Context

T = TypeVar("T")


class RunContext(Context):
    def __init__(self, session: Session, registry: Registry) -> None:
        self._session = session
        self._registry = registry

    @property
    def session_id(self) -> str:
        return self._session.id

    @property
    def history(self) -> list[Message]:
        return self._session.history

    @property
    def interrupted(self) -> bool:
        return self._session.interrupted

    def state(self, cls: type[T]) -> T:
        return self._session.state(cls)

    def add_message(self, message: Message) -> None:
        self._session.history.append(message)
        self.emit(MessageAdded(message))

    def emit(self, event: Event) -> None:
        for hook in self._registry.all("hook"):
            hook.on(event, self)

    def get(self, kind: str) -> object | None:
        return self._registry.get(kind)

    def all(self, kind: str) -> list[object]:
        return self._registry.all(kind)