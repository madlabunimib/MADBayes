import numpy as np
from numba import njit
from ..structures import Graph


def DFS(graph: Graph) -> np.ndarray:
    adjacency_matrix = graph.get_adjacency_matrix()
    n = adjacency_matrix.shape[0]
    color = np.ones(n, dtype=bool)
    times = -np.ones((n, 2), dtype=int)
    parents = -np.ones(n, dtype=int)
    _DFS(n, adjacency_matrix, color, times, parents)
    dfs = {'parents': parents, 'times': times}
    return dfs

@njit
def _DFS(n: int, A: np.ndarray, color: np.ndarray, times: np.ndarray, parents: np.ndarray) -> None:
    time = 0
    for i in range(n):
        if color[i]:
            time = _DFS_Visit(i, time, n, A, color, times, parents)

@njit
def _DFS_Visit(node: int, time: int, n: int, A: np.ndarray, color: np.ndarray, times: np.ndarray, parents: np.ndarray) -> int:
    color[node] = False
    times[node, 0] = time
    time = time + 1
    for i in range(n):
        if A[node][i] and color[i]:
            parents[i] = node
            time = _DFS_Visit(i, time, n, A, color, times, parents)
    times[node, 1] = time
    return time + 1
