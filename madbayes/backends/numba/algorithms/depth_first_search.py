from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numba import njit

if TYPE_CHECKING:
    from typing import Dict
    from ....structures import Graph


def DFS(graph: Graph) -> Dict:
    A = graph.adjacency_matrix()
    n = A.shape[0]
    color = np.ones(n, dtype=bool)
    times = -np.ones((n, 2), dtype=int)
    parents = -np.ones(n, dtype=int)
    _DFS(A, color, times, parents)
    return {'parents': parents, 'times': times}


@njit(cache=True)
def _DFS(
    A: np.ndarray,
    color: np.ndarray,
    times: np.ndarray,
    parents: np.ndarray
) -> None:
    time = 0
    n = A.shape[0]
    for i in range(n):
        if color[i]:
            time = _DFS_Visit(i, time, A, color, times, parents)


@njit
def _DFS_Visit(
    node: int,
    time: int,
    A: np.ndarray,
    color: np.ndarray,
    times: np.ndarray,
    parents: np.ndarray
) -> int:
    n = A.shape[0]
    color[node] = False
    times[node, 0] = time
    time = time + 1
    for i in range(n):
        if A[node][i]:
            if color[i]:
                parents[i] = node
                time = _DFS_Visit(i, time, A, color, times, parents)
    times[node, 1] = time
    return time + 1
