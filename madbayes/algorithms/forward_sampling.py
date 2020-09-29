from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from random import uniform

from ..backend import BayesianNetwork, topological_sorting
from ..structures import Dataset

if TYPE_CHECKING:
    from typing import List, Set


def forward_sampling(bn: BayesianNetwork, size: int):
    samples = []
    sorting = topological_sorting(bn)

    for _ in range(size):
        sample = {}

        for Xi in sorting:
            index = {k: v for k, v in sample.items() if k in bn.parents(Xi)}
            table = bn(Xi).sel(index)

            i = 0
            cumulative = table[0]
            while uniform(0, 1) > cumulative and i < len(table) - 1:
                cumulative += table[i]
                i += 1
            sample[Xi] = bn.get_levels(Xi)[i]
        
        samples.append(sample)

    return Dataset(samples)
