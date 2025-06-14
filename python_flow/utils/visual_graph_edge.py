from __future__ import annotations

from typing import Optional


class GraphEdge:
    DEFAULT_WIDTH = "1"
    WIDTH_FOR_COMBINED_EDCGES = "3"
    COLOR_FOR_COMBINED_EDGES = "black"
    STYLE_FOR_ASYNC_EDGES = "dashed"
    STYLE_FOR_CONSECUTIVE_EDGES = "solid"

    def __init__(
        self,
        source_node_label: str,
        sink_node_label: str,
        color: str,
        is_async: bool,
        label: Optional[str],
    ):
        self.source_node_label = source_node_label
        self.sink_node_label = sink_node_label
        self.color = color
        self.style = self.STYLE_FOR_ASYNC_EDGES if is_async else self.STYLE_FOR_CONSECUTIVE_EDGES
        self.width = self.DEFAULT_WIDTH
        self.label = label

    def add_to_graphviz(self, graph):
        graph.edge(
            self.source_node_label,
            self.sink_node_label,
            penwidth=self.width,
            color=self.color,
            label=self.label,
            style=self.style,
        )

    def mark_as_combined_edge(self):
        self.color = self.COLOR_FOR_COMBINED_EDGES
        self.width = self.WIDTH_FOR_COMBINED_EDCGES

    def __eq__(self, value: GraphEdge) -> bool:
        return self.source_node_label == value.source_node_label and self.sink_node_label == value.sink_node_label
