from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..backends import alternative_backend
from .nodes import _children

if TYPE_CHECKING:
    from typing import List


@alternative_backend()
def _all_simple_paths(source: int, target: int, A: np.ndarray) -> List:
    visited = [source]
    simple_paths = _all_simple_paths_recursive(source, target, A, visited)
    return simple_paths
    
def _all_simple_paths_recursive(source: int, target: int, A: np.ndarray, visited: np.ndarray) -> List:
    visited = visited + [source]
    if source == target:
        return [visited]
    else:
        simple_paths = []
        children = _children(source, A)
        children = set(children).difference(set(visited))
        for child in children:
            simple_paths += _all_simple_paths_recursive(child, target, A, visited)
        return simple_paths
