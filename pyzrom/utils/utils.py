from typing import List

from pyzrom.base import AsyncPipeline
from pyzrom.utils.visual_graph_edge import GraphEdge

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

def initialize_all_pipelines(pipelines: List[AsyncPipeline]):
    for pipeline in pipelines:
        pipeline.initialize()

def remove_duplicates(edges: List[GraphEdge]):
    seen_edges = []
    for edge in edges:
        if edge not in seen_edges:
            seen_edges.append(edge)
    return seen_edges

def render_graphviz_graph(pipelines: List[AsyncPipeline], label: str = "pyzrom_graph"):
    import graphviz

    graph = graphviz.Digraph(label, format="png")
    edges = []
    for color_index, pipeline in enumerate(pipelines):
        edges += pipeline.create_pipeline_edges(color=COLORS[color_index % len(COLORS)])
    
    unique_edges = remove_duplicates(edges)

    for edge in unique_edges:
        if edges.count(edge) > 1:
            edge.mark_as_combined_edge()
        edge.add_to_graphviz(graph)
    
    graph.render(filename=f"{label}.gv")

