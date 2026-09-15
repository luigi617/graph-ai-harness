from __future__ import annotations

from protocols.approver import Approver
from protocols.mediator import Context


class AutoApprove(Approver):
    """Approve every ask — for non-interactive/automated runs."""

    def approve(self, call: dict, reason: str, ctx: Context) -> bool:
        return True


class ConsoleApprover(Approver):
    """
    Prompt on the terminal: y (once) / n (deny) / a (always allow this tool).
    """

    def __init__(self) -> None:
        self._always: set[str] = set()

    def approve(self, call: dict, reason: str, ctx: Context) -> bool:
        name = call.get("name", "")
        if name in self._always:
            return True
        args = call.get("arguments", {})
        answer = input(f"{reason} {name}({args}) [y/n/a]: ").strip().lower()
        if answer == "a":
            self._always.add(name)
            return True
        return answer == "y"
