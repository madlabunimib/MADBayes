import numpy as np
from numba import njit
from numba.typed import Dict
from .nodes import _neighbors, _fill_in_set
from ..structures import Graph
from ..utils import union, intersection, difference

def MCS(graph: Graph, return_new_edges: bool = False) -> np.ndarray:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    adjacency_matrix = graph.get_adjacency_matrix()
    new_edges = np.zeros(adjacency_matrix.shape, dtype=bool)
    _MCS(0, adjacency_matrix, new_edges)
    triangulated = Graph(graph.get_nodes(), adjacency_matrix)
    if return_new_edges:
        return triangulated, new_edges
    return triangulated

# @njit(cache=True)
def _MCS(node: int, A: np.ndarray, out: np.ndarray) -> np.ndarray:
    i = 1
    n = A.shape[0]
    while i < n:
        if i == 1:
            numbering = np.array([node])
            X = np.array([i for i in range(n)])
        i += 1
        X = difference(X, numbering)
        x = X.shape[0]
        vmax = -1
        pmax = -1
        for j in range(x):
            k = len(intersection(_neighbors(X[j], A), numbering))
            if vmax < k:
                vmax = k
                pmax = j
        numbering = np.append(numbering, [X[pmax]])
        nodes = intersection(_neighbors(X[pmax], A), numbering[:i])
        indices = _fill_in_set(nodes, A)
        m = indices.shape[0]
        if m > 0:
            for l in range(m):
                out[indices[l, 0], indices[l, 1]] = True
            np.bitwise_or(out, A, A)
            i = 1
