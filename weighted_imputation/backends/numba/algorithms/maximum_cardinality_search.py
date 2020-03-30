import numpy as np
from numba import njit
from numba.typed import Dict

from ....structures import Graph
from ..utils import difference, intersection, union
from .nodes import _fill_in_set, _filter, _neighbors
from .paths import _all_simple_paths


def MCS(graph: Graph) -> Graph:
    adjacency_matrix = graph.adjacency_matrix()
    out = np.zeros(adjacency_matrix.shape, dtype=bool)
    _MCS(0, adjacency_matrix, out)
    triangulated = Graph(graph.nodes(), adjacency_matrix)
    return triangulated

@njit(cache=True)
def _MCS(node: int, A: np.ndarray, out: np.ndarray) -> np.ndarray:
    i = 1
    n = A.shape[0]
    while i < n:
        if i == 1:
            numbering = np.array([node])
            X = np.array([i for i in range(n)])
            # Caching neighbors
            neighbors = Dict()
            for j in range(n):
                neighbors[X[j]] = _neighbors(X[j], A)
        i += 1
        X = difference(X, numbering)
        x = X.shape[0]
        vmax = -1
        pmax = -1
        for j in range(x):
            k = len(intersection(neighbors[X[j]], numbering))
            if vmax < k:
                vmax = k
                pmax = j
        numbering = np.append(numbering, [X[pmax]])
        nodes = intersection(neighbors[X[pmax]], numbering[:i])
        if _add_missing_edges(nodes, A, out):
            i = 1

@njit(cache=True)
def _add_missing_edges(nodes: np.ndarray, A: np.ndarray, out: np.ndarray) -> bool:
    indices = _fill_in_set(nodes, A)
    n = indices.shape[0]
    if n > 0:
        for i in range(n):
            out[indices[i, 0], indices[i, 1]] = True
        np.bitwise_or(out, A, A)
        return True
    return False
