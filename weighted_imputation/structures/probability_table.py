from typing import Dict, List, Tuple

import numpy as np
import xarray as xa


class ProbabilityTable():

    _table: xa.DataArray
     
    def __init__(self, data: np.ndarray = None, variables: List[str] = None, levels: List[List[str]] = None) -> None:
        self._table = xa.DataArray(data=data, dims=variables, coords=levels)
    
    def __call__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.variables():
                raise KeyError('"{}" is not a valid key.'.format(key))
        location = tuple([
            kwargs.get(variable, slice(None))
            for variable in self.variables()
        ])
        return self._table.loc[location]
    
    def variables(self) -> List[str]:
        return self._table.dims
    
    def __repr__(self):
        return str(self._table)

    def __abs__(self):
        out = type(self)()
        out._table = abs(self._table)
        return out

    def __add__(self, other):
        out = type(self)()
        out._table = self._table + other
        return out
    
    def __floordiv__(self, other):
        out = type(self)()
        out._table = self._table // other
        return out
    
    def __mod__(self, other):
        out = type(self)()
        out._table = self._table % other
        return out

    def __mul__(self, other):
        out = type(self)()
        out._table = self._table * other
        return out
    
    def __matmul__(self, other):
        out = type(self)()
        out._table = self._table @ other
        return out
    
    def __neg__(self):
        out = type(self)()
        out._table = - self._table
        return out
    
    def __pos__(self):
        out = type(self)()
        out._table = + self._table
        return out
    
    def __pow__(self, other):
        out = type(self)()
        out._table = self._table ** other
        return out
    
    def __sub__(self, other):
        out = type(self)()
        out._table = self._table - other
        return out
    
    def __truediv__(self, other):
        out = type(self)()
        out._table = self._table / other
        return out
    
    @classmethod
    def from_xarray(cls, data: xa.DataArray):
        pt = cls()
        pt._table = data
        return pt
