from __future__ import annotations

import time

from core.events import Event, IterationStarted, ResponseReceived
from protocols.hook import Hook
from protocols.mediator import Context


class IterationCounter(Hook):
    """Record the loop's iteration index into the run extra."""

    def on(self, event: Event, ctx: Context) -> None:
        if isinstance(event, IterationStarted):
            ctx.extra["iterations"] = event.index


class ElapsedTime(Hook):
    """Track seconds elapsed since the first event, in the run extra."""

    def on(self, event: Event, ctx: Context) -> None:
        now = time.monotonic()
        ctx.extra.setdefault("started_at", now)
        ctx.extra["elapsed"] = now - ctx.extra["started_at"]


class CostCounter(Hook):
    """Accumulate the running cost (USD) from each response into the run extra."""

    def on(self, event: Event, ctx: Context) -> None:
        if isinstance(event, ResponseReceived):
            ctx.extra["cost"] = ctx.extra.get("cost", 0.0) + event.response.cost
