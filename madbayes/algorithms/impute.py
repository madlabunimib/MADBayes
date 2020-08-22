from __future__ import annotations
from .junction_tree import junction_tree
from ..structures import Dataset
from copy import deepcopy
import pandas as pd

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List
    from ..backend import BayesianNetwork


def impute(network: BayesianNetwork, dataset: Dataset) -> Dataset:
    jt = junction_tree(network)
    data = deepcopy(dataset.data)
    nans = data[data.isnull().any(axis=1)]
    cache = {}
    for index, row in nans.iterrows():
        query = row.to_dict()
        evidence = {
            k: v
            for k, v in query.items()
            if not pd.isnull(v)
        }
        key = str(evidence)
        if key not in cache.keys():
            query = sorted(query.keys() - evidence.keys())
            jte = jt.set_evidence(**evidence)
            query = jte.query('joint', query)[0]
            query = [
                query.sum(set(query.dims) - set([variable]))
                for variable in query.dims
            ]
            query = {
                q.dims[0]: q.coords[q.dims[0]].values[q.argmax()]
                for q in query
            }
            cache[key] = query
        query = cache[key]
        for key, value in query.items():
            data.loc[[index], [key]] = value
    return Dataset(data)
