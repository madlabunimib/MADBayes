import numpy as np
from numba import njit
from typing import List, Set
from .nodes import _neighbors
from ..structures import Graph
from ..utils import union, intersection, difference


def bron_kerbosh(graph: Graph) -> List:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    nodes = graph.get_nodes()
    adjacency_matrix = graph.get_adjacency_matrix()
    maximal_cliques = _bron_kerbosh(adjacency_matrix)
    maximal_cliques = [
        [nodes[node] for node in maximal_clique]
        for maximal_clique in maximal_cliques
    ]
    return maximal_cliques

# Initialize jitted version of _bron_kerbosh by using empty typed sets
@njit(cache=True)
def _bron_kerbosh(adjacency_matrix: np.ndarray) -> List:
    n = adjacency_matrix.shape[0]
    A = np.array([0 for _ in range(0)])
    B = np.array([i for i in range(n)])
    C = np.array([0 for _ in range(0)])
    return _bron_kerbosh_recursive(adjacency_matrix, A, B, C)

@njit
def _bron_kerbosh_recursive(adjacency_matrix: np.ndarray, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    out = [np.array([0 for _ in range(0)]) for _ in range(0)]
    X = B.copy()
    n = X.shape[0]
    for i in range(n):
        node = np.array([X[i]])
        neighbors = _neighbors(X[i], adjacency_matrix)
        out += _bron_kerbosh_recursive(
            adjacency_matrix,
            union(A, node),
            intersection(B, neighbors),
            intersection(C, neighbors)
        )
        B = difference(B, node)
        C = union(C, node)
    return out
