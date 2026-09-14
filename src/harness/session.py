from __future__ import annotations

from dataclasses import dataclass, field

from core.ids import new_id
from core.message import Message


@dataclass
class Session:
    id: str = field(default_factory=lambda: new_id("sess"))
    history: list[Message] = field(default_factory=list)
    interrupted: bool = False
    extra: dict = field(default_factory=dict)
