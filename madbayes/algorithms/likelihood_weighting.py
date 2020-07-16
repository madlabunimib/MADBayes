from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from random import uniform
from multiprocessing import Pool, cpu_count

from . import find_topological_order
from .nodes import parents
from ..structures import BayesianNetwork, Dataset

if TYPE_CHECKING:
    from typing import List, Dict, Set


def likelihood_weighting(bn: BayesianNetwork, query: Dict, n_samples: int, evidence={}):
    order = find_topological_order(bn)

    params = [
        (bn, order, evidence)
        for _ in range(n_samples)
    ]
    pool = Pool(cpu_count())
    samples = pool.starmap(_sample, params)
    pool.close()
    pool.join()
    
    return _compute_probability(query, samples)


def _sample(bn: BayesianNetwork, order: List, evidence: Dict):
    sample = pd.Series(index=order, dtype=str)
    w = 1
    for X_i in order:
        filter = {dim: sample[dim]
                  for dim in bn[X_i]["CPT"].variables() if dim != X_i}
        probs = bn[X_i]["CPT"].sel(filter)

        if not X_i in list(evidence.keys()):
            num = uniform(0, 1)
            cum_prob = 0
            for i in range(len(probs)):
                cum_prob += probs[i]
                if num <= cum_prob:
                    x_i = bn[X_i]["CPT"].levels(X_i)[i]
                    sample._set_value(X_i, x_i)
                    break
        else:
            x_i = evidence[X_i]
            sample._set_value(X_i, x_i)
            u_i = parents(bn, X_i)
            p_u_i = {par : sample[par] for par in u_i}
            p_u_i.update({X_i : x_i})
            w *= bn[X_i]["CPT"].loc[p_u_i].values
    return sample, w


def _compute_probability(query: Dict, samples: List):
    numerator = denominator = 0
    for sample in samples:
        denominator += sample[1]
        num = True
        for q in query:
            if not sample[0].loc[q] == query[q]:
                num = False
                break
        if num:
            numerator += sample[1]
    return numerator / denominator
