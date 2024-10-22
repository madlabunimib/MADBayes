import numpy as np
from numba import njit
from numba.typed import List

from ..utils import IntegerList, IntegerVector, difference, intersection, union
from .nodes import _children


@njit(cache=True)
def _all_simple_paths(source: int, target: int, A: np.ndarray) -> List:
    out = IntegerList()
    visited = IntegerVector()
    _all_simple_paths_recursive(source, target, A, visited, out)
    return out


@njit(cache=True)
def _all_simple_paths_recursive(source: int, target: int, A: np.ndarray, visited: np.ndarray, out: List) -> None:
    current = np.array([source])
    visited = np.append(visited, current)
    if source == target:
        out.append(visited)
    else:
        children = _children(source, A)
        children = difference(children, visited)
        n = len(children)
        for i in range(n):
            _all_simple_paths_recursive(children[i], target, A, visited, out)
