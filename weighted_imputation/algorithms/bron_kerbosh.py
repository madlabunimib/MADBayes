import numpy as np
from math import ceil
from numba import njit
from typing import List
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

@njit(cache=True)
def _bron_kerbosh_recursive(adjacency_matrix: np.ndarray, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    out = [np.array([0 for _ in range(0)]) for _ in range(0)]
    X = B.copy()
    n = B.shape[0]
    # Select a pivot vertex
    pivot = 0
    if n > 0:
        pivot = _bron_kerbosh_pivot(adjacency_matrix, X)
    for i in range(n):
        node = np.array([X[i]])
        neighbors = _neighbors(X[i], adjacency_matrix)
        if len(np.argwhere(neighbors == pivot)) == 0:
            out += _bron_kerbosh_recursive(
                adjacency_matrix,
                union(A, node),
                intersection(B, neighbors),
                intersection(C, neighbors)
            )
            B = difference(B, node)
            C = union(C, node)
    return out

@njit(cache=True)
def _bron_kerbosh_pivot(adjacency_matrix: np.ndarray, X: np.ndarray) -> int:
    n = X.shape[0]
    # Calculate degrees of nodes
    degrees = np.zeros(n)
    for i in range(n):
        degrees[i] = len(_neighbors(i, adjacency_matrix))
    # Select the pivot vertex by maximum degree
    pivot = np.argmax(degrees)
    return pivot
