from typing import Dict, List

import numpy as np
import xarray as xa

from .probability_table import ProbabilityTable


class JointProbabilityTable(ProbabilityTable):
    
    __slots__ = []

    def margins(self, variables: List[str]) -> ProbabilityTable:
        over = [v for v in self.variables() if v not in variables]
        if len(over) > 0:
            return self.sum(over)
        return self.copy()
