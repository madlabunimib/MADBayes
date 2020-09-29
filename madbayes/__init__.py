from .backend import *

# Experimental classmethod crossreference dynamic binding
from .utils.plot import plot
Graph.plot = plot
from .io.parser import from_file
DiscreteBayesianNetwork.from_file = from_file

from . import data, utils
from .algorithms import (bds_score, expectation_maximization, forward_sampling,
                         hill_climbing, impute, LikelihoodWeighting, structural_em, JunctionTree)
from .structures import (Dataset)
