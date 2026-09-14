from __future__ import annotations

from core.message import Message
from graph import Graph
from protocols.tracer import Tracer


class GraphTracer(Tracer):
    """
    Records each node into a caller-owned graph as the run unfolds.
    """

    def __init__(self, graph: Graph) -> None:
        self._graph = graph
        self._last: str | None = None
        self._owner: dict[str, str] = {}  # tool call id -> assistant node id

    def on_node(self, node: Message) -> None:
        self._graph.add_node(node.id, data=node)

        # Sequence backbone: link to the previous node.
        if self._last is not None:
            self._graph.add_edge(self._last, node.id, role="next")
        self._last = node.id

        # Remember which assistant turn owns each tool call.
        for call in node.tool_calls:
            cid = call.get("id")
            if cid:
                self._owner[cid] = node.id

        # Provenance: a tool result points back to the call that produced it.
        if node.tool_use_id and node.tool_use_id in self._owner:
            self._graph.add_edge(
                self._owner[node.tool_use_id],
                node.id,
                role="tool_result",
                call_id=node.tool_use_id,
                name=node.name,
            )
