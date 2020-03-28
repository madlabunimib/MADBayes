from typing import Dict, List

import numpy as np
import xarray as xa

from .probability_table import ProbabilityTable


class JointProbabilityTable(ProbabilityTable):
    
    __slots__ = []

    def margins(self, variables: List[str]) -> ProbabilityTable:
        levels = [list(self.levels(v)) for v in variables]
        pt = ProbabilityTable(dims=variables, coords=levels)

        for location in pt.locations():
            # TODO: Find a way to remove the medium pointer
            pointer = tuple([*location.values()])
            pt.loc[pointer] = self(**location).sum()

        return pt
