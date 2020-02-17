import numpy as np
from numba import njit, prange
from itertools import combinations
from ..structure import Graph


def moralize(graph: Graph) -> Graph:
    A = graph.get_adjacency_matrix()
    out = np.zeros(A.shape, dtype=bool)
    _moralize(A, out)
    graph.set_adjacency_matrix(out)
    return graph


@njit(parallel=True)
def _moralize(A, out):
    n = A.shape[0]
    for columns in prange(n):
        parents = A.T[columns]
        indexes = np.nonzero(parents)[0].T
        for i in indexes:
            for j in indexes:
                if i != j:
                    out[i, j] = True
    np.bitwise_or(A, out, out)
    np.bitwise_or(out, out.T, out)
