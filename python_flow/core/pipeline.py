from typing import Any, Awaitable, Callable, List, Optional

from python_flow.core import AsyncNode, Node
from python_flow.core.enums import PipelineState
from python_flow.utils.visual_graph_edge import GraphEdge


class AsyncPipeline:
    def __init__(
        self,
        head: AsyncNode,
        middle_nodes: List[Node],
        create_task_callback: Optional[Callable[[Awaitable], Any]] = None,
    ):
        self._head = head
        self._nodes = [head] + middle_nodes
        self._state = PipelineState.UNINITIALIZED
        self._tasks = []
        self._create_task = create_task_callback
        if self._create_task is None:
            import asyncio

            self._create_task = asyncio.create_task

    def initialize(self):
        for node_index, node in enumerate(self._nodes[:-1]):
            sink = self._nodes[node_index + 1]
            if sink not in node.sinks:
                node.set_sink(sink)
        self._state = PipelineState.WAITING

    async def start(self):
        if self._state == PipelineState.UNINITIALIZED:
            raise RuntimeError("Pipeline needs to be initialized first")
        if self._state == PipelineState.RUNNING:
            raise RuntimeError("Pipeline is already running")

        for node in self._nodes[1:]:
            if issubclass(type(node), AsyncNode):
                self._tasks.append(self._create_task(node.start()))
        self._state = PipelineState.RUNNING
        self._create_task(self._head.start())

    def create_pipeline_edges(self, color: str) -> List[GraphEdge]:
        edges = []
        for node_index, node in enumerate(self._nodes[:-1]):
            sink = self._nodes[node_index + 1]
            edge = GraphEdge(
                node.label,
                sink.label,
                color=color,
                is_async=issubclass(type(sink), AsyncNode),
                label=node.input_type,
            )
            edges.append(edge)
        return edges
