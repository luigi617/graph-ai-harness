from __future__ import annotations

from dataclasses import dataclass, field

from protocols.provider import Message


@dataclass
class Session:
    history: list[Message] = field(default_factory=list)
    interrupted: bool = False
