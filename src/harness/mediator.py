from __future__ import annotations

from core.message import Message
from harness.registry import Registry
from harness.session import Session


class Context:
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

    def add_message(self, message: Message) -> None:
        self._session.history.append(message)
        for observer in self._registry.all("tracer"):
            observer.on_node(message)

    def get(self, kind: str) -> object | None:
        return self._registry.get(kind)

    def all(self, kind: str) -> list[object]:
        return self._registry.all(kind)
