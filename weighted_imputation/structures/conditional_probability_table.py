import numpy as np
import pandas as pd
from typing import List


class CPT():

    _cpt: pd.DataFrame
     
    def __init__(self, dependant: str, dependencies: List[str], data: np.ndarray = None, levels: List[str] = None, tuples: List = None) -> None:
        if data is None:
            n = len(dependencies) + 1
            data = np.zeros((n, n))
        if len(dependencies) == 0:
            self._cpt = pd.DataFrame(
                data=data,
                index=levels,
                columns=[dependant]
            ).T
        else:
            index = None
            if tuples is not None:
                index = pd.MultiIndex.from_tuples(
                    tuples,
                    names=dependencies
                )
            self._cpt = pd.DataFrame(
                data=data,
                index=index,
                columns=levels
            )
    
    def __repr__(self):
        return str(self._cpt)
