import numpy as np
from itertools import combinations
from ..structure import Graph


def moralize(graph: Graph) -> Graph:
    A = graph.get_adjacency_matrix()
    graph.set_adjacency_matrix(_moralize(A))
    return graph


def _moralize(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    N = np.zeros((n, n), dtype=bool)
    for parents in A.T:
        parents = np.nonzero(parents)[0].T
        parents = combinations(parents, 2)
        for (i, j) in parents:
            N[i, j] = True
    R = np.bitwise_or(A, N)
    R = np.bitwise_or(R, R.T)
    return R
