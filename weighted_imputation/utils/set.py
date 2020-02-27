import numpy as np


def union(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a.shape) != 1 or len(b.shape) != 1:
        raise Exception('Arrays must be 1D.')
    out = np.concatenate((a, b))
    out = np.unique(out)
    return out

def intersection(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a.shape) != 1 or len(b.shape) != 1:
        raise Exception('Arrays must be 1D.')
    out = np.concatenate((a, b))
    out = np.bincount(out)
    out = np.argwhere(out > 1)
    out = out.T[0]
    return out

def difference(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if len(a.shape) != 1 or len(b.shape) != 1:
        raise Exception('Arrays must be 1D.')
    pass
