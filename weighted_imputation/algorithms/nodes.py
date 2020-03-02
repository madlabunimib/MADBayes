import numpy as np
from numba import njit

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
def _ancestors(node: int, A: np.ndarray) -> np.ndarray:
    parents = np.array([node])
    ancestors = _ancestors_recursive(parents, A)
    return ancestors

@njit(cache=True)
def _ancestors_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    n = nodes.shape[0]
    if n == 0:
        return nodes
    if n == 1:
        return _parents(nodes[0], A)
    ancestors = np.array([0 for _ in range(0)])
    for i in range(n):
        ancestors = np.append(
            ancestors,
            _ancestors_recursive(nodes[i:i+1])
        )
    ancestors = np.unique(ancestors)
    return ancestors

@njit(cache=True)
def _descendants(node: int, A: np.ndarray) -> np.ndarray:
    parents = np.array([node])
    descendants = _descendants_recursive(parents, A)
    return descendants

@njit(cache=True)
def _descendants_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    n = nodes.shape[0]
    if n == 0:
        return nodes
    if n == 1:
        return _children(nodes[0], A)
    descendants = np.array([0 for _ in range(0)])
    for i in range(n):
        descendants = np.append(
            descendants,
            _descendants_recursive(nodes[i:i+1])
        )
    descendants = np.unique(descendants)
    return descendants
