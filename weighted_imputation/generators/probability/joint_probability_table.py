import numpy as np


def generate_joint_probability_table(N):
    numBins = 3
    data = np.random.randn(1000, N)
    jpt, edges = np.histogramdd(data, bins=numBins)
    jpt /= jpt.sum()
    return jpt