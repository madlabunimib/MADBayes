import numpy as np
from numba import njit
from typing import List, Set
from ..structures import Graph
from ..utils import union, intersection, difference


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
    A = np.array([0 for _ in range(0)])
    B = np.array(nodes_indexes)
    C = np.array([0 for _ in range(0)])
    return _bron_kerbosh(adjacency_matrix, A, B, C)

@njit
def _neighbor_set(adjacency_matrix: np.ndarray, node: int) -> np.ndarray:
    A = adjacency_matrix[node]
    neighbor_set = np.nonzero(A)[0].T
    return neighbor_set

@njit(parallel=True)
def _bron_kerbosh(adjacency_matrix: np.ndarray, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> List:
    if len(B) == 0 and len(C) == 0:
        return [A]
    result = [np.array([0 for _ in range(0)]) for _ in range(0)]
    X = B.copy()
    n = len(X)
    for i in range(n):
        node = np.array([X[i]])
        neighbor_set = _neighbor_set(adjacency_matrix, X[i])
        result += _bron_kerbosh(
            adjacency_matrix,
            union(A, node),
            intersection(B, neighbor_set),
            intersection(C, neighbor_set)
        )
        B = difference(B, node)
        C = union(C, node)
    return result
