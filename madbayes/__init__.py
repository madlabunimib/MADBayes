from .backend import *

# Import as reference for retrocompatibility
from .backend import CliqueTree as JunctionTree

# Experimental classmethod crossreference dynamic binding
from .utils.plot import plot
Graph.plot = plot
from .io.parser import from_file
DiscreteBayesianNetwork.from_file = from_file

from . import data, utils
from .algorithms import (bds_score, expectation_maximization, forward_sampling,
                         hill_climbing, impute, structural_em, LikelihoodWeighting)
from .structures import (Dataset)
