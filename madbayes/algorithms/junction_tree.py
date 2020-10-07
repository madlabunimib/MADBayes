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
        if isinstance(network, BayesianNetwork):
            self._calibrate_upward(None, self.root)
            self._calibrate_downward(None, self.root, xa.DataArray(1))

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
        self._calibrate_downward(None, str(clique), xa.DataArray(1))

    def _calibrate_upward(self, _prev: str, _curr: str) -> xa.DataArray:
        message = reduce(mul, [
            self._calibrate_upward(_curr, _next)
            for _next in self.neighbors(_curr)
            if _next != _prev
        ], xa.DataArray(1))

        clique = self.get_clique(_curr)

        if clique.is_separator or not clique.belief.dims:
            clique.belief = message
            self.set_clique(clique)
            return message

        clique.belief = clique.belief * message
        self.set_clique(clique)

        margin = frozenset()
        if _prev is not None:
            margin = frozenset(self.get_clique(_prev).nodes)
            margin = frozenset(clique.nodes).difference(margin)
        
        return clique.belief.sum(margin)

    def _calibrate_downward(self, _prev: str, _curr: str, message: xa.DataArray) -> None:
        clique = self.get_clique(_curr)

        if clique.is_separator:
            margin = frozenset(clique.nodes)
            margin = frozenset(message.dims).difference(margin)
            message = message.sum(margin) / clique.belief

        clique.belief = clique.belief * message
        self.set_clique(clique)

        if not clique.is_separator:
            message = clique.belief

        for _next in self.neighbors(_curr):
            if _next != _prev:
                self._calibrate_downward(_curr, _next, message)
