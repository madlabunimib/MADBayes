from typing import List

import numpy as np
import xarray as xa


class CPT():

    _cpt: xa.DataArray
    _dependant: str
    _dependencies: List[str]
     
    def __init__(self, data: xa.DataArray) -> None:
        self._cpt = data.copy()
        # self._dependant = variables[0]
        # self._dependencies = variables[1::]
    
    def get_dependant(self) -> str:
        return self._dependant
    
    def get_dependencies(self) -> List[str]:
        return self._dependencies
    
    def __repr__(self):
        return str(self._cpt)
