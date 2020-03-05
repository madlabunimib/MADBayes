import numpy as np
from numba import njit
from numba.typed import Dict
from .nodes import _neighbors, _fill_in_set
from ..structures import Graph
from ..utils import union, intersection, difference


def maximum_cardinality_search(graph: Graph) -> np.ndarray:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    nodes = graph.get_nodes()
    adjacency_matrix = graph.get_adjacency_matrix()
    numbering = _maximum_cardinality_search(0, adjacency_matrix)
    numbering = [nodes[i] for i in numbering]
    return numbering

@njit(cache=True)
def _maximum_cardinality_search(node: int, A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    neighbors = Dict()
    numbering = np.array([node])
    X = np.array([i for i in range(n)])
    for i in range(n):
        # Caching neighbors sets
        neighbors[X[i]] = _neighbors(X[i], A)
    for i in range(1, n):
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
    return numbering

def maximum_cardinality_search_fill_in(graph: Graph, return_new_edges: bool = False) -> np.ndarray:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    adjacency_matrix = graph.get_adjacency_matrix()
    new_edges = np.zeros(adjacency_matrix.shape, dtype=bool)
    _maximum_cardinality_search_fill_in(0, adjacency_matrix, new_edges)
    triangulated = Graph(graph.get_nodes(), adjacency_matrix)
    if return_new_edges:
        return triangulated, new_edges
    return triangulated

@njit(cache=True)
def _maximum_cardinality_search_fill_in(node: int, A: np.ndarray, out: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    numbering = np.array([node])
    X = np.array([i for i in range(n)])
    for i in range(1, n):
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
        for l in range(m):
            out[indices[l, 0], indices[l, 1]] = True
    np.bitwise_or(out, A, A)
