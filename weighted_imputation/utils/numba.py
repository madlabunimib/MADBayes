import numpy as np
from numba import njit
from numba.typed import List
from numba.types import int64

_int = int64
_sequence_int = _int[:]


@njit(cache=True)
def IntegerVector(iterable=None):
    out = np.array([], dtype=_int)
    if iterable is not None:
        out = np.array(iterable, dtype=_int)
    return out


@njit(cache=True)
def IntegerList(iterable=None):
    out = List.empty_list(item_type=_sequence_int)
    if iterable is not None:
        out.extend(iterable)
    return out
