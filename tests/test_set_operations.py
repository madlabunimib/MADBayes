import numpy as np
from . import weighted_imputation as wi

def test_set():
    a = [0, 1, 2, 3]
    b = [2, 3, 4, 5]
    # Test union
    x = set(a).union(set(b))
    x = sorted(list(x))
    y = wi.utils.set.union(np.array(a), np.array(b))
    y = sorted(list(y))
    assert(x == y)
    # Test intersection
    x = set(a).intersection(set(b))
    x = sorted(list(x))
    y = wi.utils.set.intersection(np.array(a), np.array(b))
    y = sorted(list(y))
    assert(x == y)
    # Test difference
    x = set(a).difference(set(b))
    x = sorted(list(x))
    y = wi.utils.set.difference(np.array(a), np.array(b))
    y = sorted(list(y))
    assert(x == y)
