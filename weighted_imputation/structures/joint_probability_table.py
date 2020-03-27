from typing import Dict, List

import numpy as np
import xarray as xa

from .probability_table import ProbabilityTable


class JointProbabilityTable(ProbabilityTable):
     
    def __init__(self, data: np.ndarray = None, variables: List[str] = None, levels: List[List[str]] = None) -> None:
        super().__init__(data, variables, levels)
