from __future__ import annotations

from core.guard import GuardDecision
from plugins.hooks.counters import CostState, ElapsedState, IterationState
from protocols.guard import Guard
from protocols.mediator import Context


class MaxIterations(Guard):
    """
    Stop once the iteration count reaches the limit.
    Pair with an IterationCounter hook, which populates IterationState.
    """

    def __init__(self, limit: int) -> None:
        self._limit = limit

    def check(self, ctx: Context) -> GuardDecision:
        if ctx.state(IterationState).index >= self._limit:
            return GuardDecision.halt(f"reached {self._limit} iterations")
        return GuardDecision.proceed()


class Timeout(Guard):
    """
    Stop once elapsed time exceeds the budget.
    Pair with an ElapsedTime hook, which populates ElapsedState.
    """

    def __init__(self, seconds: float) -> None:
        self._seconds = seconds

    def check(self, ctx: Context) -> GuardDecision:
        if ctx.state(ElapsedState).elapsed >= self._seconds:
            return GuardDecision.halt(f"exceeded {self._seconds}s time budget")
        return GuardDecision.proceed()


class BudgetGuard(Guard):
    """
    Stop once accumulated cost (USD) reaches the budget.
    Pair with a CostCounter hook, which populates CostState.
    """

    def __init__(self, max_cost: float) -> None:
        self._max_cost = max_cost

    def check(self, ctx: Context) -> GuardDecision:
        if ctx.state(CostState).total >= self._max_cost:
            return GuardDecision.halt(f"exceeded ${self._max_cost} budget")
        return GuardDecision.proceed()
