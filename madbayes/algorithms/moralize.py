from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..backends import AlternativeBackend
from ..structures import Graph
from .nodes import _parents

if TYPE_CHECKING:
    from ..structures import DirectedGraph


@AlternativeBackend()
def moralize(graph: DirectedGraph) -> Graph:
    A = graph.adjacency_matrix()
    new_edges = np.zeros(A.shape, dtype=bool)
    _moralize(A, new_edges)
    moral = Graph(graph.nodes(), A)
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
