import numpy as np
from numba import njit, prange
from ..structure import Graph


def moralize(graph: Graph, force_parallel: bool = False, return_new_edges: bool = False) -> Graph:
    A = graph.get_adjacency_matrix()
    new_edges = np.zeros(A.shape, dtype=bool)
    if not force_parallel and A.shape[0] < 50:
        _moralize(A, new_edges)
    else:
        _moralize_parallel(A, new_edges)
    moral_graph = Graph(graph.get_nodes(), A)
    if return_new_edges:
        return moral_graph, new_edges
    return moral_graph


@njit(cache=True)
def _moralize(A, out):
    n = A.shape[0]
    for columns in range(n):
        parents = A.T[columns]
        indexes = np.nonzero(parents)[0].T
        for i in indexes:
            for j in indexes:
                if i < j:
                    out[i, j] = True
    np.bitwise_or(out, A, A)
    np.bitwise_or(A, A.T, A)


@njit(parallel=True)
def _moralize_parallel(A, out):
    n = A.shape[0]
    for columns in prange(n):
        parents = A.T[columns]
        indexes = np.nonzero(parents)[0].T
        for i in indexes:
            for j in indexes:
                if i < j:
                    out[i, j] = True
    np.bitwise_or(out, A, A)
    np.bitwise_or(A, A.T, A)
