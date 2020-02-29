import numpy as np
from numba import njit
from typing import List
from math import log, ceil
from ..structures import Graph


def DFS(graph: Graph) -> np.ndarray:
    adjacency_matrix = graph.get_adjacency_matrix()
    n = adjacency_matrix.shape[0]
    color = np.ones(n, dtype=bool)
    times = -np.ones((n, 2), dtype=int)
    parents = -np.ones(n, dtype=int)
    _DFS(n, adjacency_matrix, color, times, parents)
    return {'parents': parents, 'times': times}

@njit(cache=True)
def _DFS(
        n: int,
        A: np.ndarray,
        color: np.ndarray,
        times: np.ndarray,
        parents: np.ndarray
    ) -> None:
    time = 0
    for i in range(n):
        if color[i]:
            time = _DFS_Visit(i, time, n, A, color, times, parents)

@njit
def _DFS_Visit(
        node: int,
        time: int,
        n: int,
        A: np.ndarray,
        color: np.ndarray,
        times: np.ndarray,
        parents: np.ndarray
    ) -> int:
    color[node] = False
    times[node, 0] = time
    time = time + 1
    for i in range(n):
        if A[node][i]:
            if color[i]:
                parents[i] = node
                time = _DFS_Visit(i, time, n, A, color, times, parents)
    times[node, 1] = time
    return time + 1

# Sparse Table
def ST(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    m = ceil(log(n)/log(2))
    B = np.zeros((n, m), dtype=int)
    for i in range(n):
        B[i, 0] = i
    j = 1
    while (1 << j) < n:
        i = 0
        while i + (1 << (j-1)) < n:
            l = B[i, j-1]
            r = B[i + (1 << (j-1)), j-1]
            if A[l] <= A[r]:
                B[i, j] = l
            else:
                B[i, j] = r
            i += 1
        j += 1
    return B

# Range Minimum Query
@njit(cache=True)
def RMQ(L: int, R: int, A: np.ndarray, ST: np.ndarray) -> int:
    j = int(log(R - L + 1)/log(2))
    i = R - (1 << j) + 1
    if A[ST[L, j]] <= A[ST[i, j]]:
        return A[ST[L, j]]
    return A[ST[i, j]]
