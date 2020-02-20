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
    nodes = sorted(nodes)
    n = len(nodes)
    adjacency_matrix = np.zeros((n, n), dtype=bool)
    for parent, child in edges:
        i = nodes.index(parent)
        j = nodes.index(child)
        adjacency_matrix[i, j] = True
    return Graph(nodes, adjacency_matrix)
