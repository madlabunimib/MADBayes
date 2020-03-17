from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numba import njit, prange

from ....structures import Graph
from .nodes import _parents

if TYPE_CHECKING:
    from ....structures import DirectedGraph


def moralize(graph: DirectedGraph) -> Graph:
    A = graph.get_adjacency_matrix()
    new_edges = np.zeros(A.shape, dtype=bool)
    _moralize(A, new_edges)
    moral = Graph(graph.get_nodes(), A)
    return moral

@njit(cache=True, parallel=True)
def _moralize(A: np.ndarray, out: np.ndarray) -> None:
    n = A.shape[0]
    for node in prange(n):
        parents = _parents(node, A)
        for i in parents:
            for j in parents:
                if i < j:
                    out[i, j] = True
    np.bitwise_or(out, A, A)
    np.bitwise_or(A, A.T, A)
