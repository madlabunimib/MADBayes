from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from random import uniform
from multiprocessing import Pool, cpu_count
from itertools import product

from ..backend import BayesianNetwork
from .find_topological_ordering import find_topological_order

if TYPE_CHECKING:
    from typing import List, Dict, Set, Tuple


def likelihood_weighting(bn: BayesianNetwork, method: str, query: Dict, n_samples: int, evidence={}):
    # Find topological order for the Bayesian Network
    order = find_topological_order(bn)
    # Create samples with weights
    params = [
        (bn, order, evidence)
        for _ in range(n_samples)
    ]
    pool = Pool(cpu_count())
    samples = pool.starmap(_sample, params)
    pool.close()
    pool.join()

    if method == 'marginal':
        params = [
            (bn, [var], samples)
            for var in query
        ]
        pool = Pool(cpu_count())
        probs = pool.starmap(_compute_probability, params)
        pool.close()
        pool.join()
        return probs

    if method == 'joint':
        return _compute_probability(bn, query, samples)


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
            u_i = bn.parents(X_i)
            p_u_i = {par: sample[par] for par in u_i}
            p_u_i.update({X_i: x_i})
            w *= bn[X_i]["CPT"].loc[p_u_i].values
    return sample, w


def _compute_probability(bn: BayesianNetwork, query: List, samples: List):
    queries = _my_product({X_i: bn.levels(X_i) for X_i in query})
    probs = {}

    for query in queries:
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
        probs.update({str(query): numerator / denominator})
    return probs


def _my_product(input: Dict[Tuple]):
    return (dict(zip(input.keys(), values)) for values in product(*input.values()))
