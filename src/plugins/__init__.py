from __future__ import annotations

from harness import GraphAIHarness
from plugins.context_manager import SummarizingContextManager
from plugins.guards import BudgetGuard, MaxIterations, Timeout
from plugins.hooks import CostCounter, ElapsedTime, IterationCounter
from plugins.loops import AgenticLoop, ChatLoop
from plugins.permissions import (
    AllowList,
    AskUnless,
    AutoApprove,
    ConsoleApprover,
    DenyList,
)
from plugins.providers import BaseProvider, BedrockProvider
from plugins.tracers import GraphTracer

__all__ = [
    "default_harness",
    "ChatLoop",
    "AgenticLoop",
    "SummarizingContextManager",
    "BaseProvider",
    "BedrockProvider",
    "GraphTracer",
    "AllowList",
    "DenyList",
    "AskUnless",
    "AutoApprove",
    "ConsoleApprover",
    "MaxIterations",
    "Timeout",
    "BudgetGuard",
    "IterationCounter",
    "ElapsedTime",
    "CostCounter",
]


def default_harness() -> GraphAIHarness:
    return GraphAIHarness().use(AgenticLoop()).use(SummarizingContextManager())
