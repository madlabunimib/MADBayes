from .backend import *

# Experimental import as reference for retrocompatibility
from .backend import CliqueTree as JunctionTree

# Experimental classmethod crossreference dynamic binding
from .utils.plot import plot
Graph.plot = plot
from .io.parser import from_file
DiscreteBayesianNetwork.from_file = from_file

from . import data, utils
from .algorithms import (bds_score, expectation_maximization, hill_climbing, impute, structural_em, LikelihoodWeighting)
from .structures import (Dataset)

# Experimental hybrid return type
from .backend import forward_sampling as _forward_sampling
def forward_sampling(model: DiscreteBayesianNetwork, size: int):
    return Dataset(_forward_sampling(model, size))
