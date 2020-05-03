from copy import deepcopy
from itertools import product
from typing import Dict, List, Tuple

import numpy as np
import xarray as xa


class ProbabilityTable(xa.DataArray):

    __slots__ = []

    def __init__(
            self,
            data=None,
            coords=None,
            dims=None,
            name=None,
            attrs=None,
            indexes=None,
            fastpath=False
        ) -> None:
        
        if dims is not None:
            dims = tuple(dims)

        super().__init__(
            data=data,
            coords=coords,
            dims=dims,
            name=name,
            attrs=attrs,
            indexes=indexes,
            fastpath=fastpath
        )
    
    def __call__(self, **kwargs):
        location = tuple([
            kwargs.get(variable, slice(None))
            for variable in self.dims
        ])
        return self.loc[location]
    
    def variables(self) -> Tuple[str]:
        return self.dims
    
    def levels(self, variable: str) -> Tuple[str]:
        return tuple(self.coords[variable].values)
    
    def locations(self, variables=None) -> Tuple[Dict]:
        if variables is None:
            variables = self.variables()
        levels = (
            self.levels(variable)
            for variable in variables
        )
        locations = product(*levels)
        locations = (
            dict(zip(variables, location))
            for location in locations
        )
        return locations
    
    def marginalize(self, variables: List[str]) -> 'ProbabilityTable':
        over = [v for v in self.variables() if v not in variables]
        if len(over) > 0:
            return self.sum(over)
        return self.copy()
    
    def fillna(self, value):
        indices = np.isnan(self.values)
        self.values[indices] = value
        return self
    
    def sort(self):
        variables = sorted(self.variables())
        out = self.sortby(
            variables = variables
        )
        out = type(self)(
            out.values,
            dims = variables,
            coords = tuple(
                out.coords[variable].values
                for variable in variables
            )
        )
        return out

    @classmethod
    def from_data(cls, data, variables, levels):
        return cls(data=data, dims=variables, coords=levels)
    
    @classmethod
    def from_probability_table(cls, pt):
        return cls(
            data=np.copy(pt.values),
            dims=deepcopy(pt.dims),
            coords=deepcopy(pt.coords)
        )
