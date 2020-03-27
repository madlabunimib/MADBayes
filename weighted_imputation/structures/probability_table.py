from typing import Dict, List, Tuple

import numpy as np
import xarray as xa


class ProbabilityTable(xa.DataArray):

    __slots__ = []
    
    def __call__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.dims:
                raise KeyError('"{}" is not a valid key.'.format(key))
        location = tuple([
            kwargs.get(variable, slice(None))
            for variable in self.dims
        ])
        return self.loc[location]
    
    def variables(self) -> List[str]:
        return self.dims
    
    @classmethod
    def from_data(cls, data, variables, levels):
        return cls(data=data, dims=variables, coords=levels)
