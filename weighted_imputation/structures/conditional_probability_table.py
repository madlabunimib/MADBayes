from typing import Dict, List

import numpy as np
import xarray as xa

from .probability_table import ProbabilityTable


class ConditionalProbabilityTable(ProbabilityTable):
     
    def __init__(self, data: np.ndarray, variables: List[str], levels: List[List[str]]) -> None:
        super().__init__(data, variables, levels)
    
    def dependant(self) -> str:
        return self._variables[0]
    
    def dependencies(self) -> List[str]:
        return self._variables[1::]
