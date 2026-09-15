from __future__ import annotations

from harness import GraphAIHarness
from plugins.context_manager import SummarizingContextManager
from plugins.guards import BudgetGuard, MaxIterations, Timeout
from plugins.hooks import CostCounter, ElapsedTime, IterationCounter
from plugins.loops import AgenticLoop, ChatLoop
from plugins.memory import FileMemoryStore
from plugins.permissions import (
    AllowList,
    AskUnless,
    AutoApprove,
    ConsoleApprover,
    DenyList,
)
from plugins.providers import BedrockProvider
from plugins.spawner import InProcessSpawner
from plugins.tools import Forget, Recall, Remember, Subagent
from plugins.tracers import GraphTracer

__all__ = [
    "AgenticLoop",
    "AllowList",
    "AskUnless",
    "AutoApprove",
    "BedrockProvider",
    "BudgetGuard",
    "ChatLoop",
    "ConsoleApprover",
    "CostCounter",
    "DenyList",
    "ElapsedTime",
    "FileMemoryStore",
    "Forget",
    "GraphTracer",
    "InProcessSpawner",
    "IterationCounter",
    "MaxIterations",
    "Recall",
    "Remember",
    "Subagent",
    "SummarizingContextManager",
    "Timeout",
    "default_harness",
]


def default_harness() -> GraphAIHarness:
    return GraphAIHarness().use(AgenticLoop()).use(SummarizingContextManager())
