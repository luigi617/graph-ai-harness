from __future__ import annotations

from core.guard import GuardDecision
from protocols.guard import Guard
from protocols.mediator import Context


class MaxIterations(Guard):
    """
    Stop once the iteration count reaches the limit.
    Pair with an IterationCounter hook, which populates extra["iterations"].
    """

    def __init__(self, limit: int) -> None:
        self._limit = limit

    def check(self, ctx: Context) -> GuardDecision:
        if ctx.extra.get("iterations", 0) >= self._limit:
            return GuardDecision.halt(f"reached {self._limit} iterations")
        return GuardDecision.proceed()


class Timeout(Guard):
    """
    Stop once elapsed time exceeds the budget.
    Pair with an ElapsedTime hook, which populates extra["elapsed"].
    """

    def __init__(self, seconds: float) -> None:
        self._seconds = seconds

    def check(self, ctx: Context) -> GuardDecision:
        if ctx.extra.get("elapsed", 0.0) >= self._seconds:
            return GuardDecision.halt(f"exceeded {self._seconds}s time budget")
        return GuardDecision.proceed()
