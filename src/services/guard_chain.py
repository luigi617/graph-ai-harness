from __future__ import annotations

from core.guard import GuardDecision
from protocols.guard import Guard
from protocols.mediator import Context


class GuardChain:
    """Consults every registered guard; the first to halt stops the loop."""

    def check(self, ctx: Context) -> GuardDecision:
        for guard in ctx.all(Guard):
            decision = guard.check(ctx)
            if decision.stop:
                return decision
        return GuardDecision.proceed()
