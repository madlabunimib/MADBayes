import numpy as np
from numba import njit
from numba.typed import Dict
from .nodes import _neighbors, _fill_in_set
from ..structures import Graph
from ..utils import union, intersection, difference

def maximum_cardinality_search_numbering(graph: Graph) -> np.ndarray:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    nodes = graph.get_nodes()
    adjacency_matrix = graph.get_adjacency_matrix()
    numbering = _maximum_cardinality_search_numbering(0, adjacency_matrix)
    numbering = [nodes[i] for i in numbering]
    return numbering

@njit(cache=True)
def _maximum_cardinality_search_numbering(node: int, A: np.ndarray) -> np.ndarray:
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
