from __future__ import annotations

from dataclasses import dataclass

from core.message import Message
from core.response import Response


class Event:
    """Base class for hook events."""


@dataclass
class IterationStarted(Event):
    index: int


@dataclass
class ResponseReceived(Event):
    response: Response


@dataclass
class MessageAdded(Event):
    message: Message
