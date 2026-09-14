from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

from core.ids import new_id
from core.message import Message

T = TypeVar("T")


@dataclass
class Session:
    id: str = field(default_factory=lambda: new_id("sess"))
    history: list[Message] = field(default_factory=list)
    interrupted: bool = False
    _state: dict[type, object] = field(default_factory=dict)

    def state(self, cls: type[T]) -> T:
        """
        Return this session's instance of ``cls``, creating a default on
        first access.
        """
        inst = self._state.get(cls)
        if inst is None:
            inst = cls()
            self._state[cls] = inst
        return inst  # type: ignore[return-value]
