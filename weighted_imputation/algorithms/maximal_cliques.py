import numpy as np
from numba import njit
from typing import List, Set
from ..structure import Graph


def maximal_cliques(graph: Graph) -> List:
    nodes = graph.get_nodes()
    nodes_indexes = [i for i, _ in enumerate(nodes)]
    adjacency_matrix = graph.get_adjacency_matrix()
    maximal_cliques = _bron_kerbosh(adjacency_matrix, set(), set(nodes_indexes), set())
    maximal_cliques = [
        [nodes[node] for node in maximal_clique]
        for maximal_clique in maximal_cliques
    ]
    return maximal_cliques

@njit
def _neighbor_set(adjacency_matrix: np.ndarray, node: int) -> Set[int]:
    A = adjacency_matrix[node]
    neighbor = np.nonzero(A)[0].T
    neighbor_set = set(neighbor)
    return neighbor_set

def _bron_kerbosh(adjacency_matrix: np.ndarray, A: Set[int], B: Set[int], C: Set[int]) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    result = []
    for node in B.copy():
        neighbor_set = _neighbor_set(adjacency_matrix, node)
        result += _bron_kerbosh(
            adjacency_matrix,
            A.union({node}),
            B.intersection(neighbor_set),
            C.intersection(neighbor_set)
        )
        B = B.difference({node})
        C = C.union({node})
    return result
