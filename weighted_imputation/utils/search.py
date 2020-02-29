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

@njit(cache=True)
def _times_parents_to_euler_tour(times: np.array, parents: np.ndarray) -> List:
    euler_tour = []
    # Check if the graph is connected,
    # otherwise no euler tour exists
    roots = np.count_nonzero(parents < 0)
    if roots > 1:
        return euler_tour
    n = times.shape[0]
    # Fill a stack with the nodes ordered by discover times
    stack = np.argsort(times.T[0])
    # Iterate over the stack following the order of discovery
    for i in range(n):
        # Add the node in the euler tour
        euler_tour.append(stack[i])
        # The next node in the stack can be:
        # 1) A child of the current node (i == parents[i+1])
        # 2) A sibling of the current node (i != parents[i+1] and parents[i] == parents[i+1])
        # 3) A child of a common ancestor (i != parents[i+1] and parents[i] != parents[i+1])
        # For scenario 3 (and 2) we need to backtrack until scenario 1 is true.
        # Additionally, we need to backtrack also when last node is reached (i == n-1),
        # in this case the halting condition is parents[i] != root.
        if i == n-1 or (i < n-1 and stack[i] != parents[stack[i+1]]):
            x = stack[i]
            halt = stack[0]
            if i < n-1:
                halt = parents[stack[i+1]]
            while x != halt:
                # Backtraking from child to parent
                x = parents[x]
                euler_tour.append(x)
    return euler_tour

# Sparse Table
def ST(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    m = ceil(log(n)/log(2))
    out = np.zeros((n, m), dtype=int)
    _ST(n, m, A, out)
    return out
    
@njit(cache=True)
def _ST(n: int, m: int, A: np.ndarray, out: np.ndarray) -> None:
    for i in range(n):
        out[i, 0] = i
    j = 1
    while (1 << j) < n:
        i = 0
        while i + (1 << (j-1)) < n:
            l = out[i, j-1]
            r = out[i + (1 << (j-1)), j-1]
            if A[l] <= A[r]:
                out[i, j] = l
            else:
                out[i, j] = r
            i += 1
        j += 1

# Range Minimum Query
@njit(cache=True)
def RMQ(L: int, R: int, A: np.ndarray, sparse_table: np.ndarray) -> int:
    j = int(log(R - L + 1)/log(2))
    i = R - (1 << j) + 1
    if A[sparse_table[L, j]] <= A[sparse_table[i, j]]:
        return A[sparse_table[L, j]]
    return A[sparse_table[i, j]]

# Lowest Common Ancestor with RMQ of Euler Tour
@njit(cache=True)
def LCA(a: int, b: int, euler_tour: np.ndarray, sparse_table: np.ndarray) -> int:
    Fa = np.where(euler_tour == a)[0][0]
    Fb = np.where(euler_tour == b)[0][0]
    if Fa > Fb:
        return RMQ(Fb, Fa, euler_tour, sparse_table)
    return RMQ(Fa, Fb, euler_tour, sparse_table)

def find_cycles(graph: Graph) -> List:
    adjacency_matrix = graph.get_adjacency_matrix()
    dfs = DFS(graph)
    times = dfs['times']
    parents = dfs['parents']
    return _find_cycles(adjacency_matrix, parents, graph.is_directed())

@njit(cache=True)
def _find_cycles(A: np.ndarray, parents: np.ndarray, is_directed: bool) -> List:
    cycles = []
    if not is_directed:
        A = np.triu(A)
    edges = np.argwhere(A)
    n = edges.shape[0]
    for k in range(n):
        i, j = edges[k]
        if A[i][j]:
            if i != parents[j] and j != parents[i]:
                cycle = _find_cycle(i, j, parents)
                cycles.append(cycle)
    return cycles

@njit
def _find_cycle(a: int, b: int, parents: np.ndarray) -> List:
    lca = []
    while a != -1:
        lca.append(a)
        a = parents[a]
    lca = lca[::-1]
    cycle = []
    while b not in lca:
        cycle.append(b)
        b = parents[b]
    b = lca.index(b)
    cycle += lca[b:] 
    return cycle
