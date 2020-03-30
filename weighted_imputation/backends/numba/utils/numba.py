import numpy as np
from numba import njit, typeof
from numba.typed import Dict, List
from numba.types import int64

_int = int64
_int_sequence = _int[:]


@njit(cache=True)
def IntegerVector(iterable=None):
    out = np.array([0 for _ in range(0)], dtype=_int)
    if iterable is not None:
        out = np.array(iterable, dtype=_int)
    return out


@njit(cache=True)
def IntegerList(iterable=None):
    out = List.empty_list(item_type=_int_sequence)
    if iterable is not None:
        out.extend(iterable)
    return out


_int_vector = typeof(IntegerVector())


@njit(cache=True)
def IntegerVectorDict():
    out = Dict.empty(key_type=_int, value_type=_int_vector)
    return out
