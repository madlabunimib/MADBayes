from typing import Dict, List, Set

import numpy as np

from ..structures import Graph
from .nodes import _neighbors


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

def _bron_kerbosh(adjacency_matrix: np.ndarray) -> List:
    n = adjacency_matrix.shape[0]
    A = set()
    B = set(range(n))
    C = set()
    # Caching neighbors
    neighbors = {i: set(_neighbors(i, adjacency_matrix)) for i in range(n)}
    return _bron_kerbosh_recursive(neighbors, A, B, C)

def _bron_kerbosh_recursive(neighbors: Dict, A: Set, B: Set, C: Set) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    out = []
    X = B.copy()
    n = len(B)
    # Select a pivot vertex
    pivot = 0
    if n > 0:
        pivot = _bron_kerbosh_pivot(neighbors, B, C)
    for node in X:
        if pivot not in neighbors[node]:
            out += _bron_kerbosh_recursive(
                neighbors,
                A.union({node}),
                B.intersection(neighbors[node]),
                C.intersection(neighbors[node])
            )
            B = B.difference({node})
            C = C.union({node})
    return out

def _bron_kerbosh_pivot(neighbors: Dict, B: Set, C: Set) -> int:
    # Select the pivot vertex by Cazals-Karande method
    X = B.union(C)
    pivot = {key: neighbors[key] for key in X}
    pivot = {key: value.intersection(B) for key, value in pivot.items()}
    pivot = max(pivot, key=pivot.get)
    return pivot
