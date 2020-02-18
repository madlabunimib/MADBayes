import numpy as np
from numba import njit, prange
from ..structure import Graph


def moralize(graph: Graph, force_parallel: bool = False) -> Graph:
    A = graph.get_adjacency_matrix()
    out = np.zeros(A.shape, dtype=bool)
    if not force_parallel and A.shape[0] < 50:
        _moralize(A, out)
    else:
        _moralize_parallel(A, out)
    return Graph(graph.get_nodes(), out)


@njit
def _moralize(A, out):
    n = A.shape[0]
    for columns in range(n):
        parents = A.T[columns]
        indexes = np.nonzero(parents)[0].T
        for i in indexes:
            for j in indexes:
                if i != j:
                    out[i, j] = True
    np.bitwise_or(A, out, out)
    np.bitwise_or(out, out.T, out)


@njit(parallel=True)
def _moralize_parallel(A, out):
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
