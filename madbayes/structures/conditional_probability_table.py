from typing import Dict, List

import numpy as np
import xarray as xa

from .probability_table import ProbabilityTable


class ConditionalProbabilityTable(ProbabilityTable):

    __slots__ = []

    def dependant(self) -> str:
        return self.variables()[0]

    def dependencies(self) -> List[str]:
        return self.variables()[1::]
