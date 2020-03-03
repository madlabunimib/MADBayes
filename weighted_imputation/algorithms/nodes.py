import numpy as np
from numba import njit
from ..utils import union, intersection, difference

@njit(cache=True)
def _parents(node: int, A: np.ndarray) -> np.ndarray:
    parents = A.T[node]
    parents = np.nonzero(parents)[0].T
    return parents

@njit(cache=True)
def _family(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    family = np.append(parents, [node])
    return family

@njit(cache=True)
def _children(node: int, A: np.ndarray) -> np.ndarray:
    children = A[node]
    children = np.nonzero(children)[0].T
    return children

@njit(cache=True)
def _neighbors(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    children = _children(node, A)
    neighbors = np.append(parents, children)
    neighbors = np.unique(neighbors)
    return neighbors

@njit(cache=True)
def _boundary(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    n = len(nodes)
    boundary = np.array([0 for _ in range(0)])
    if n == 0:
        return boundary
    for i in range(n):
        neighbors = _neighbors(nodes[i], A)
        boundary = np.append(boundary, neighbors)
    boundary = np.unique(boundary)
    boundary = difference(boundary, nodes)
    return boundary

@njit(cache=True)
def _ancestors(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    ancestors = _ancestors_recursive(parents, A)
    return ancestors

@njit(cache=True)
def _ancestors_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    n = len(nodes)
    ancestors = nodes
    if n == 0:
        return ancestors
    for i in range(n):
        parents = _parents(nodes[i], A)
        ancestors = np.append(
            ancestors,
            _ancestors_recursive(parents, A)
        )
    ancestors = np.unique(ancestors)
    return ancestors

@njit(cache=True)
def _descendants(node: int, A: np.ndarray) -> np.ndarray:
    children = _children(node, A)
    descendants = _descendants_recursive(children, A)
    return descendants

@njit(cache=True)
def _descendants_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    n = len(nodes)
    descendants = nodes
    if n == 0:
        return descendants
    for i in range(n):
        children = _children(nodes[i], A)
        descendants = np.append(
            descendants,
            _descendants_recursive(children, A)
        )
    descendants = np.unique(descendants)
    return descendants

@njit(cache=True)
def _numbering(nodes: np.ndarray) -> np.ndarray:
    # An array is ordered so that numbering(i) is
    # actually the i-th nodes, using the array index
    numbering = np.array(nodes, copy=True)
    return numbering

@njit(cache=True)
def _is_complete(A: np.ndarray) -> bool:
    out = A.copy()
    np.fill_diagonal(out, True)
    return out.all()

@njit(cache=True)
def _is_complete_set(nodes: np.ndarray, A: np.ndarray) -> bool:
    out = A[nodes, :][:, nodes]
    return _is_complete(out)

@njit(cache=True)
def _fill_in(A: np.array) -> np.ndarray:
    out = A.copy()
    np.fill_diagonal(out, True)
    np.bitwise_not(out, out)
    indexes = np.argwhere(out)
    return indexes

@njit(cache=True)
def _fill_in_set(nodes: np.ndarray, A: np.array) -> np.ndarray:
    out = A[nodes, :][:, nodes]
    indexes = _fill_in(out)
    # Convert relative indexes to absolute indexes
    n = indexes.shape[0]
    for i in range(n):
        indexes[i, 0] = nodes[indexes[i, 0]]
        indexes[i, 1] = nodes[indexes[i, 1]]
    return indexes
