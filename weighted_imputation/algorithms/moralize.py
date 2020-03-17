import numpy as np

from ..structures import DirectedGraph, Graph
from .nodes import _parents


def moralize(graph: DirectedGraph) -> Graph:
    if not isinstance(graph, DirectedGraph):
        raise Exception('graph must be istance of DirectedGraph class.')
    A = graph.get_adjacency_matrix()
    new_edges = np.zeros(A.shape, dtype=bool)
    _moralize(A, new_edges)
    moral = Graph(graph.get_nodes(), A)
    return moral

def _moralize(A: np.ndarray, out: np.ndarray):
    n = A.shape[0]
    for node in range(n):
        parents = _parents(node, A)
        for i in parents:
            for j in parents:
                if i < j:
                    out[i, j] = True
    np.bitwise_or(out, A, A)
    np.bitwise_or(A, A.T, A)
