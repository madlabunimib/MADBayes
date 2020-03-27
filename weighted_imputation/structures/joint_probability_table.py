from typing import Dict, List

import numpy as np
import xarray as xa

from .probability_table import ProbabilityTable


class JointProbabilityTable(ProbabilityTable):
    
    __slots__ = []

    def marginalize(self, variables: List[str]) -> ProbabilityTable:
        levels = [list(self.levels(v)) for v in variables]
        pt = ProbabilityTable(dims=variables, coords=levels)

        # TODO: Check if JPT must be transposed or it's optional
        order = variables + [v for v in self.variables() if v not in variables]
        jpt = self.transpose(*order)

        for location in pt.locations():
            # TODO: Find a way to remove the medium pointer
            pointer = tuple([*location.values()])
            pt.loc[pointer] = jpt(**location).sum()

        return pt
