import numpy as np

from ..backends import AlternativeBackend
from ..structures import Graph
from .nodes import _fill_in_set, _filter, _neighbors
from .paths import _all_simple_paths


@AlternativeBackend()
def MCS(graph: Graph) -> Graph:
    adjacency_matrix = graph.adjacency_matrix()
    out = np.zeros(adjacency_matrix.shape, dtype=bool)
    _MCS(0, adjacency_matrix, out)
    triangulated = Graph(graph.nodes(), adjacency_matrix)
    return triangulated

def _MCS(node: int, A: np.ndarray, out: np.ndarray) -> np.ndarray:
    raise NotImplementedError('This function MUST be refactored.')
    i = 1
    n = A.shape[0]
    while i < n:
        if i == 1:
            X = set(range(n))
            numbering = set()
            numbering.add(node)
            neighbors = {i: set(_neighbors(i, A)) for i in range(n)}
        i += 1
        X = X.difference(numbering)
        xmax = {key: neighbors[key] for key in X}
        xmax = {key: value.intersection(numbering) for key, value in xmax.items()}
        xmax = {key: len(value) for key, value in xmax.items()}
        xmax = max(xmax, key=xmax.get)
        numbering.add(xmax)
        nodes = np.array(list(neighbors[xmax].intersection(numbering)), dtype=int)
        if _add_missing_edges(nodes, A, out):
            i = 1

# TODO: Refactor _MCS to remove this function
def _add_missing_edges(nodes: np.ndarray, A: np.ndarray, out: np.ndarray) -> bool:
    indices = _fill_in_set(nodes, A)
    n = indices.shape[0]
    if n > 0:
        for i in range(n):
            out[indices[i, 0], indices[i, 1]] = True
        np.bitwise_or(out, A, A)
        return True
    return False
