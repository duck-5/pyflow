from typing import List

from python_flow.core import AsyncPipeline
from python_flow.core.enums import LoggingSeverity
from python_flow.utils.visual_graph_edge import GraphEdge

COLORS = [
    "forestgreen",
    "limegreen",
    "turquoise",
    "lightseagreen",
    "cornflowerblue",
    "darkblue",
    "purple",
    "fuchsia",
    "orchid",
    "firebrick",
    "orangered",
    "lightsalmon",
    "gold",
    "burlywood",
    "lightslategray",
]


async def async_start_pipelines(pipelines: List[AsyncPipeline]):
    for pipeline in pipelines:
        await pipeline.start()


def get_logging_callback_by_severity(logger, severity: LoggingSeverity):
    return getattr(logger, severity.name.lower())


def initialize_all_pipelines(pipelines: List[AsyncPipeline]):
    for pipeline in pipelines:
        pipeline.initialize()


def remove_duplicates(edges: List[GraphEdge]):
    seen_edges = []
    for edge in edges:
        if edge not in seen_edges:
            seen_edges.append(edge)
    return seen_edges


def render_graphviz_graph(pipelines: List[AsyncPipeline], label: str = "python_flow_graph"):
    import os

    import graphviz

    os.environ["PATH"] += os.pathsep + r"D:\ProgramFiles\Graphviz-13.0.0-win32\bin"

    graph = graphviz.Digraph(label, format="png")
    edges = []
    for color_index, pipeline in enumerate(pipelines):
        edges += pipeline.create_pipeline_edges(color=COLORS[color_index % len(COLORS)])

    unique_edges = remove_duplicates(edges)

    for edge in unique_edges:
        if edges.count(edge) > 1:
            edge.mark_as_combined_edge()
        edge.add_to_graphviz(graph)

    graph.attr(dpi="300")
    graph.render(filename=f"{label}.gv")
