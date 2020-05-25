from __future__ import annotations

import numpy as np
import pandas as pd

from ..structures import Dataset
from .junction_tree import junction_tree

from multiprocessing import Pool, cpu_count

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List
    from ..structures import BayesianNetwork, JunctionTree


def impute(network: BayesianNetwork, dataset: Dataset) -> Dataset:
    jt = junction_tree(network)
    cols = dataset.columns()
    data = dataset.data.copy()
    nans = data[data.isnull().any(axis=1)]
    nans = nans.astype(str, copy=False).groupby(cols).indices

    nans = [
        (jt, dict(zip(cols, values)), indices)
        for values, indices in nans.items()
    ]

    pool = Pool(cpu_count())
    nans = pool.starmap(_impute_nans, nans)
    pool.close()
    pool.join()

    for (query, indices) in nans:
        data.loc[indices, query.keys()] = list(query.values())
    return Dataset(data)


def _impute_nans(jt: JunctionTree, query: Dict, indices: List):
    evidence = {
        k: v
        for k, v in query.items()
        if v != str(np.nan)
    }
    query = list(query.keys() - evidence.keys())
    jte = jt.set_evidence(**evidence)
    query = jte.query('joint', query)[0]
    query = [
        query.marginalize([variable])
        for variable in query.variables()
    ]
    query = {
        q.dims[0]: q.coords[q.dims[0]].values[q.argmax()]
        for q in query
    }
    return (query, indices)
