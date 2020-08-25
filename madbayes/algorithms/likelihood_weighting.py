from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from random import uniform
from itertools import product

from ..backend import BayesianNetwork, topological_sorting
from .inference_system import InferenceSystem

if TYPE_CHECKING:
    from typing import Any, List, Dict, Set, Tuple


class LikelihoodWeighting(InferenceSystem):

    def __init__(self, network: BayesianNetwork, *args, **kwargs) -> None:
        self.bn = network
        if 'size' not in kwargs:
            raise ValueError('Missing "size" keyword parameter.')
        self.size = kwargs['size']

    def query(self, variables: List, evidence: Any, method: str) -> Any:
        # Find topological order for the Bayesian Network
        order = topological_sorting(self.bn)
        # Create samples with weights
        samples = [
            self._sample(self.bn, order, evidence)
            for _ in range(self.size)
        ]

        if method == 'marginal':
            probs = [
                self._compute_probability(self.bn, [var], samples)
                for var in variables
            ]
            return probs

        if method == 'joint':
            return [self._compute_probability(self.bn, variables, samples)]


    def _sample(self, bn: BayesianNetwork, order: List, evidence: Dict):
        w = 1
        sample = {}
        for X_i in order:
            filter = {dim: sample[dim] for dim in bn(X_i).dims if dim != X_i}
            probs = bn(X_i).sel(filter)

            if not X_i in list(evidence.keys()):
                num = uniform(0, 1)
                cum_prob = 0
                for i in range(len(probs)):
                    cum_prob += probs[i]
                    if num <= cum_prob:
                        x_i = bn.get_levels(X_i)[i]
                        sample[X_i] = x_i
                        break
            else:
                x_i = evidence[X_i]
                sample[X_i] = x_i
                u_i = bn.parents(X_i)
                p_u_i = {par: sample[par] for par in u_i}
                p_u_i.update({X_i: x_i})
                w *= bn(X_i).loc[p_u_i].values
        return sample, w


    def _compute_probability(self, bn: BayesianNetwork, query: List, samples: List):
        queries = self._my_product({X_i: bn.get_levels(X_i) for X_i in query})
        probs = {}

        for query in queries:
            numerator = denominator = 0
            for sample in samples:
                denominator += sample[1]
                num = True
                for q in query:
                    if not sample[0][q] == query[q]:
                        num = False
                        break
                if num:
                    numerator += sample[1]
            probs.update({str(query): numerator / denominator})
        return probs


    def _my_product(self, input: Dict[Tuple]):
        return (dict(zip(input.keys(), values)) for values in product(*input.values()))
