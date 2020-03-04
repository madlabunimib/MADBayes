import numpy as np
from numba import njit, prange
from .nodes import _parents
from ..structures import Graph, DirectedGraph


def moralize(graph: DirectedGraph, return_new_edges: bool = False) -> Graph:
    if not isinstance(graph, DirectedGraph):
        raise Exception('graph must be istance of DirectedGraph class.')
    A = graph.get_adjacency_matrix()
    new_edges = np.zeros(A.shape, dtype=bool)
    _moralize(A, new_edges)
    moral = Graph(graph.get_nodes(), A)
    if return_new_edges:
        return moral, new_edges
    return moral


@njit(cache=True, parallel=True)
def _moralize(A, out):
    n = A.shape[0]
    for node in prange(n):
        parents = _parents(node, A)
        for i in parents:
            for j in parents:
                if i < j:
                    out[i, j] = True
    np.bitwise_or(out, A, A)
    np.bitwise_or(A, A.T, A)
