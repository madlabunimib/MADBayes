from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numba import njit

from ..utils import IntegerVectorDict, difference, intersection, union
from .nodes import _neighbors

if TYPE_CHECKING:
    import numpy as np
    from typing import Dict, List, Set
    from ....structures import Graph


def bron_kerbosh(graph: Graph) -> List:
    nodes = graph.nodes()
    adjacency_matrix = graph.adjacency_matrix()
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
    # Caching neighbors
    neighbors = IntegerVectorDict()
    for i in range(n):
        neighbors[i] = _neighbors(i, adjacency_matrix)
    return _bron_kerbosh_recursive(neighbors, A, B, C)

@njit(cache=True)
def _bron_kerbosh_recursive(neighbors: Dict, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    out = [np.array([0 for _ in range(0)]) for _ in range(0)]
    X = B.copy()
    n = B.shape[0]
    # Select a pivot vertex
    pivot = 0
    if n > 0:
        pivot = _bron_kerbosh_pivot(neighbors, B, C)
    for i in range(n):
        node = np.array([X[i]])
        if len(np.argwhere(neighbors[X[i]] == pivot)) == 0:
            out += _bron_kerbosh_recursive(
                neighbors,
                union(A, node),
                intersection(B, neighbors[X[i]]),
                intersection(C, neighbors[X[i]])
            )
            B = difference(B, node)
            C = union(C, node)
    return out

@njit(cache=True)
def _bron_kerbosh_pivot(neighbors: Dict, B: np.ndarray, C: np.ndarray) -> int:
    # Select the pivot vertex by Cazals-Karande method
    X = union(B, C)
    n = X.shape[0]
    degrees = np.zeros(n)
    for i in range(n):
        degrees[i] = len(intersection(B, neighbors[i]))
    pivot = np.argmax(degrees)
    return pivot
