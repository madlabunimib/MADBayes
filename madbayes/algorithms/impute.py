from __future__ import annotations
import pandas as pd

from ..structures import Dataset

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List
    from ..backend import BayesianNetwork


def impute(engine: Any, dataset: Dataset) -> Dataset:
    out = dataset.copy()
    for i, row in out.iterrows():
        # If there are any NANs, impute them
        if row.isnull().any():
            # Set query variables
            variables = [
                key
                for key, value in row.iteritems()
                if pd.isnull(value)
            ]
            # Set query evidence
            evidence = row.dropna().to_dict()
            # Execute joint query
            query = engine.query(variables, evidence, method="joint")[0]
            # Select argmax by levels
            query = query.to_dataframe("joint")
            query = query.sort_values(ascending=False, by=["joint"])
            levels, _ = next(query.iterrows())
            levels = [levels] if isinstance(levels, str) else levels
            levels = dict(zip(query.index.names, levels))
            row.update(levels)
            out.loc[i] = row
    return out
