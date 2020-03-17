from math import ceil, log
from typing import List

import numpy as np
from numba import njit


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
    j = int(log(R - L)/log(2))
    i = R - (1 << j)
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
