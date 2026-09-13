from __future__ import annotations

from harness.registry import Registry
from harness.session import Session
from protocols.provider import Message


class Context:
    def __init__(self, session: Session, registry: Registry) -> None:
        self._session = session
        self._registry = registry

    @property
    def history(self) -> list[Message]:
        return self._session.history

    @property
    def interrupted(self) -> bool:
        return self._session.interrupted

    def get(self, kind: str) -> object | None:
        return self._registry.get(kind)

    def all(self, kind: str) -> list[object]:
        return self._registry.all(kind)
