from typing import Dict, List

import numpy as np
import xarray as xa


class ProbabilityTable():

    _table: xa.DataArray
    _variables: List[str]
     
    def __init__(self, data: np.ndarray, variables: List[str], levels: List[List[str]]) -> None:
        self._table = xa.DataArray(data=data, dims=variables, coords=levels)
        self._variables = tuple(variables)
    
    def __call__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self._variables:
                raise KeyError('"{}" is not a valid key.'.format(key))
        location = tuple([
            kwargs.get(variable, slice(None))
            for variable in self._variables
        ])
        return self._table.loc[location]
    
    def __getattr__(self, name):
        if hasattr(self._table, name):
            return getattr(self._table, name)
        return self.__getattribute__(name)
    
    def variables(self) -> List[str]:
        return list(self._variables)
    
    def __repr__(self):
        return str(self._table)
