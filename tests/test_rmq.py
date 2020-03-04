import random
import numpy as np
from . import weighted_imputation as wi

def test_rmq():
    for i in range(10):
        n = random.randrange(1, 100)
        array = np.array([random.randrange(0, 100) for _ in range(n)])
        index = [i for i, _ in enumerate(array)]
        random.shuffle(index)
        index = [(i-1, i) for i in range(1, len(index), 2)]
        st = wi.ST(array)
        for (i, j) in index:
            if i < j:
                assert(wi.RMQ(i, j, array, st) == min(array[i:j]))
            else:
                assert(wi.RMQ(j, i, array, st) == min(array[j:i]))
