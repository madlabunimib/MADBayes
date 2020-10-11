from __future__ import annotations

from copy import deepcopy
from functools import reduce
from operator import mul
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import networkx as nx
import xarray as xa

from ..backend import moral, chordal, maximal_cliques,\
    maximum_cardinality_search, chain_of_cliques,\
    BayesianNetwork, CliqueTree, Clique

if TYPE_CHECKING:
    from typing import Any, Dict, List, Tuple


class JunctionTree(CliqueTree):

    def __init__(self, network: BayesianNetwork, *args, **kwargs) -> None:
        super().__init__(network)
        self.root = self.nodes[0]

    def query(self, variables: List[str], evidence: Any = None, method: str = "marginal") -> Any:
        if method not in ["marginal", "joint", "conditional"]:
            raise ValueError("Method must be either 'marginal', 'joint' or 'conditional'.")

        jt = JunctionTree(self)
        if evidence is not None:
            for key, value in evidence.items():
                jt._absorb_evidence(key, value)
        # Method Marginal
        if method == "marginal":
            out = []
            for variable in variables:
                clique = jt.get_clique_given_variables([variable])
                margin = frozenset(clique.nodes)
                margin = margin.difference(frozenset([variable]))
                clique = clique.belief.sum(margin)
                out.append(clique)
            return out
        # Method Joint or Conditional
        joint = None
        try:
            # If variables are contained in a single clique
            # marginalize over this clique
            joint = jt.get_clique_given_variables(variables).belief
        except:
            # Else, build the joint query
            joint = jt.get_joint_query("", jt.root, variables[::])
        
        margin = frozenset(joint.dims)
        margin = margin.difference(frozenset(variables))
        joint = joint.sum(margin)

        if method == "joint":
            return [joint]
        
        return [joint / joint.sum(variables[:1])]

    def _absorb_evidence(self, variable: str, value: str) -> None:
        clique = self.get_clique_given_variables([variable])
        margin = frozenset(clique.nodes)
        margin = margin.difference(frozenset([variable]))
        old_margin = clique.belief.sum(margin)
        new_margin = xa.zeros_like(old_margin)
        new_margin.loc[value] = 1
        clique.belief = clique.belief / old_margin * new_margin
        clique.belief.fillna(0)
        self.set_clique(clique)
        super().calibrate_downward("", str(clique), xa.DataArray(1))
