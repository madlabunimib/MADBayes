import numpy as np

from ..backends import AlternativeBackend


@AlternativeBackend()
def kullback_leibler_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))
