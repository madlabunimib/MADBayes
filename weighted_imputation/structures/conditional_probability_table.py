from typing import Dict, List

import numpy as np
import xarray as xa


class CPT():

    _cpt: xa.DataArray
    _variables: List[str]
     
    def __init__(self, data: np.ndarray, variables: List[str], levels: List[List[str]]) -> None:
        self._cpt = xa.DataArray(data=data, dims=variables, coords=levels)
        self._variables = tuple(variables)
    
    def __call__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self._variables:
                raise KeyError('"{}" is not a valid key.'.format(key))
        location = tuple([
            kwargs.get(variable, slice(None))
            for variable in self._variables
        ])
        return self._cpt.loc[location]
    
    def get_dependant(self) -> str:
        return self._variables[0]
    
    def get_dependencies(self) -> List[str]:
        return self._variables[1::]
    
    def __repr__(self):
        return str(self._cpt)
