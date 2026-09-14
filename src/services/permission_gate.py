from __future__ import annotations

from core.events import ApprovalRequested
from core.permission import PermissionDecision, PermissionVerdict
from protocols.mediator import Context


class PermissionGate:
    """
    Combines all permission plugins and resolves an 'ask' via the approver.
    """

    def decide(self, call: dict, ctx: Context) -> PermissionDecision:
        decision = self._combine(call, ctx)
        if decision.verdict != PermissionVerdict.ASK:
            return decision

        ctx.emit(ApprovalRequested(call, decision.reason))
        approver = ctx.get("approver")
        if approver is not None and approver.approve(call, decision.reason, ctx):
            return PermissionDecision.allow()
        return PermissionDecision.deny(decision.reason or "not approved")

    @staticmethod
    def _combine(call: dict, ctx: Context) -> PermissionDecision:
        # Precedence: any deny wins; else any ask; else allow.
        result = PermissionDecision.allow()
        for permission in ctx.all("permission"):
            decision = permission.check(call, ctx)
            if decision.verdict == PermissionVerdict.DENY:
                return decision
            if (
                decision.verdict == PermissionVerdict.ASK
                and result.verdict == PermissionVerdict.ALLOW
            ):
                result = decision
        return result
