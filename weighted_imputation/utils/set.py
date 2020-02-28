import numpy as np
from numba import njit


@njit
def union(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a.shape) != 1 or len(b.shape) != 1:
        raise Exception('Arrays must be 1D.')
    out = np.concatenate((a, b))
    out = np.unique(out)
    return out

@njit
def intersection(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a.shape) != 1 or len(b.shape) != 1:
        raise Exception('Arrays must be 1D.')
    out = np.concatenate((a, b))
    out = np.bincount(out)
    out = np.nonzero(out > 1)[0]
    out = out.T
    return out

@njit
def difference(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a.shape) != 1 or len(b.shape) != 1:
        raise Exception('Arrays must be 1D.')
    out = np.concatenate((a, b, b))
    out = np.bincount(out)
    out = np.nonzero(out == 1)[0]
    out = out.T
    return out
