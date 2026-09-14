from __future__ import annotations

from dataclasses import dataclass

from core.events import Event, IterationStarted
from protocols.hook import Hook
from protocols.mediator import Context


@dataclass
class IterationState:
    index: int = 0


class IterationCounter(Hook):
    """Record the loop's iteration index into IterationState."""

    def on(self, event: Event, ctx: Context) -> None:
        if isinstance(event, IterationStarted):
            ctx.state(IterationState).index = event.index
