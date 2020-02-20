import re
import numpy as np
from ..structure import Graph


def parse_graph_from_string(string: str) -> Graph:
    pattern = re.compile(r"\[(\w*)(?:\|(\w+[:\w+]*)){0,1}\]")
    edges = re.findall(pattern, string)
    edges = [
        (parent, child)
        for (child, parents) in edges
        for parent in parents.split(':')
        if len(parent) > 0
    ]
    nodes = set()
    for parent, child in edges:
        nodes.add(parent)
        nodes.add(child)
    nodes = list(nodes)
    graph = Graph(nodes)
    for parent, child in edges:
        graph.add_edge(parent, child)
    return graph
