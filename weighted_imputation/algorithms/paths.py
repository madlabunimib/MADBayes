import numpy as np
from numba import njit
from numba.typed import List
from numba.types import int64
from .nodes import _children
from ..utils import union, intersection, difference


_sequence_int = int64[:]
@njit(cache=True)
def _all_simple_paths(source: int, target: int, A: np.ndarray) -> List:
    out = List.empty_list(item_type=_sequence_int)
    visited = np.array([0 for _ in range(0)], dtype=int64)
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
