import numpy as np
from numba import njit
from typing import List, Set
from ..structures import Graph


def maximal_cliques(graph: Graph) -> List:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    nodes = graph.get_nodes()
    nodes_indexes = [i for i, _ in enumerate(nodes)]
    adjacency_matrix = graph.get_adjacency_matrix()
    maximal_cliques = _maximal_cliques(adjacency_matrix, nodes_indexes)
    maximal_cliques = [
        [nodes[node] for node in maximal_clique]
        for maximal_clique in maximal_cliques
    ]
    return maximal_cliques

# Initialize jitted version of _bron_kerbosh by using empty typed sets
@njit(cache=True)
def _maximal_cliques(adjacency_matrix: np.ndarray, nodes_indexes: List[int]) -> List:
    A = set([0 for _ in range(0)])
    B = set(nodes_indexes)
    C = set([0 for _ in range(0)])
    return _bron_kerbosh(adjacency_matrix, A, B, C)

@njit
def _neighbor_set(adjacency_matrix: np.ndarray, node: int) -> Set[int]:
    A = adjacency_matrix[node]
    neighbor = np.nonzero(A)[0].T
    neighbor_set = set(neighbor)
    return neighbor_set

@njit
def _bron_kerbosh(adjacency_matrix: np.ndarray, A: Set[int], B: Set[int], C: Set[int]) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    # TODO: Change reflected list to  typed list
    emptyset = set([0 for _ in range(0)])
    result = [emptyset for _ in range(0)]
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
