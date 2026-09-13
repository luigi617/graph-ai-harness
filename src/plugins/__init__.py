from __future__ import annotations

from harness import GraphAIHarness
from plugins.context_manager import DefaultContextManager
from plugins.loops import AgenticLoop, ChatLoop
from plugins.providers import BaseProvider, BedrockProvider
from plugins.tools import ToolRunner

__all__ = [
    "default_harness",
    "ChatLoop",
    "AgenticLoop",
    "DefaultContextManager",
    "ToolRunner",
    "BaseProvider",
    "BedrockProvider",
]


def default_harness() -> GraphAIHarness:
    return GraphAIHarness().use(AgenticLoop()).use(DefaultContextManager())
