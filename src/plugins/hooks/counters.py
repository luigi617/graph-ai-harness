from __future__ import annotations

import time
from dataclasses import dataclass

from core.events import Event, IterationStarted, ResponseReceived
from protocols.hook import Hook
from protocols.mediator import Context


@dataclass
class IterationState:
    index: int = 0


@dataclass
class ElapsedState:
    started_at: float | None = None
    elapsed: float = 0.0


@dataclass
class CostState:
    total: float = 0.0


class IterationCounter(Hook):
    """Record the loop's iteration index into IterationState."""

    def on(self, event: Event, ctx: Context) -> None:
        if isinstance(event, IterationStarted):
            ctx.state(IterationState).index = event.index


class ElapsedTime(Hook):
    """Track seconds elapsed since the first event, in ElapsedState."""

    def on(self, event: Event, ctx: Context) -> None:
        now = time.monotonic()
        state = ctx.state(ElapsedState)
        if state.started_at is None:
            state.started_at = now
        state.elapsed = now - state.started_at


class CostCounter(Hook):
    """Accumulate the running cost (USD) from each response into CostState."""

    def on(self, event: Event, ctx: Context) -> None:
        if isinstance(event, ResponseReceived):
            ctx.state(CostState).total += event.response.cost
