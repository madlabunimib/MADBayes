from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from random import uniform
from multiprocessing import Pool, cpu_count

from ..backend import BayesianNetwork, topological_sorting
from ..structures import Dataset

if TYPE_CHECKING:
    from typing import List, Set


def forward_sampling(bn: BayesianNetwork, n_samples: int):
    order = topological_sorting(bn)

    params = [
        (bn, order)
        for _ in range(n_samples)
    ]
    pool = Pool(cpu_count())
    samples = pool.starmap(_sample, params)
    pool.close()
    pool.join()

    return Dataset(pd.concat(samples, axis=1).T)


def _sample(bn: BayesianNetwork, order: List):
    sample = pd.Series(index=order, dtype=str)
    for var in order:
        filter = {dim: sample[dim]
                  for dim in bn[var]["CPT"].variables() if dim != var}
        probs = bn[var]["CPT"].sel(filter)

        num = uniform(0, 1)
        cum_prob = 0
        for i in range(len(probs)):
            cum_prob += probs[i]
            if num <= cum_prob:
                sample._set_value(var, bn[var]["CPT"].levels(var)[i])
                break
    return sample
