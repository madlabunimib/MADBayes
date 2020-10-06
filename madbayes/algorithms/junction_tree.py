from __future__ import annotations

from copy import deepcopy
from functools import reduce
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import networkx as nx
import xarray as xa

from .inference_system import InferenceSystem
from ..structures import Node, OrderedSet, Tree
from ..backend import moral, chordal, maximal_cliques, maximum_cardinality_search, chain_of_cliques

if TYPE_CHECKING:
    from typing import Any, Dict, List, Tuple
    from ..backend import BayesianNetwork


class JunctionTree(Tree, InferenceSystem):

    def __init__(self, network: BayesianNetwork, *args, **kwargs) -> None:
        self._nodes = {}
        self._cliques = []
        moralized = moral(network)
        triangulated = chordal(moralized)
        cliques = maximal_cliques(triangulated)
        alpha = maximum_cardinality_search(triangulated)
        chain = chain_of_cliques(cliques, alpha)
        root = self._build_junction_tree(network, chain)
        super().__init__(root)
        self._calibrate()

    def _index(self, node: Node) -> None:
        if node['type'] == 'clique':
            self._cliques.append(node)
            # For each node of a clique
            for item in node['nodes']:
                # If the node is not in the index
                # then add an empty list in the index
                if item not in self._nodes.keys():
                    self._nodes[item] = []
                # Append the node in which the clique
                # is located to the corresponding list
                self._nodes[item].append(node)
        # Repeat for each child of the node
        for child in node.children():
            self._index(child)

    def cliques(self) -> List[Node]:
        return self._cliques.copy()

    def query(self, variables: List[str], evidence: Any, method: str) -> Any:
        jt = deepcopy(self)
        for variable, value in evidence.items():
            jt._absorb_evidence(variable, value)
        if method == 'marginal':
            return [
                jt[variable][0]['belief'].sum(
                    set(jt[variable][0]['belief'].dims) - set([variable]))
                for variable in variables
            ]
        joint = jt._query_get_joint(variables)
        if method == 'joint':
            return [joint]
        condition = joint.sum(set(joint.dims) - set(variables[1:]))
        return [joint / condition]

    def _query_get_joint(self, variables: List[str]) -> xa.DataArray:
        # Check if variables are contained in a single clique
        joint = self._query_search_joint(variables)
        if joint is not None:
            return joint
        # If variables are not contained in a single clique
        return self._query_build_joint(variables)

    def _query_search_joint(self, variables: List[str]) -> xa.DataArray:
        clique = self._query_search_clique(
            variables[1:],
            self[variables[0]]
        )
        if clique is not None:
            return clique['belief'].sum(set(clique['belief'].dims) - set(variables))
        return None

    def _query_search_clique(self, variables: List[str], cliques: List[Node]) -> Node:
        if len(variables) == 0:
            if len(cliques) > 0:
                return cliques[0]
            return None
        cliques = [
            clique
            for clique in cliques
            if variables[0] in clique['nodes']
        ]
        return self._query_search_clique(variables[1:], cliques)

    def _query_build_joint(self, variables: List[str]) -> xa.DataArray:
        joint = self._query_build_joint_visit(variables[::], self.root())
        return joint.sum(set(joint.dims) - set(variables))

    def _query_build_joint_visit(self, variables: List[str], target: Node) -> xa.DataArray:
        if target['type'] == 'separator':
            clique = target.children()[0]
            message = self._query_build_joint_visit(variables, clique)
            # If the returning value is not one, this means that there
            # are variables of the query in the subtree under this separator,
            # so we need to divide the returning belief by the sepset belief
            if isinstance(message, xa.DataArray):
                message = message / target['belief']
            return message
        # Deafult returning value
        message = 1
        # Check if the current clique contains any variable of the query
        found = False
        for variable in target['nodes']:
            if variable in variables:
                variables.remove(variable)
                found = True
        # For each child, if there are variables left to be found,
        # make a recursive call
        for separator in target.children():
            if len(variables) > 0:
                message = message * \
                    self._query_build_joint_visit(variables, separator)
       # If the returning message is not one or a variable is found,
       # then multiply the message by the clique belief
        if isinstance(message, xa.DataArray) or found:
            message = message * target['belief']
        return message

    def _absorb_evidence(self, variable: str, value: str) -> None:
        # Select the first clique that constains variable
        clique = self[variable][0]
        old_margin = clique['belief'].sum(
            set(clique['belief'].dims) - set([variable]))
        new_margin = xa.zeros_like(old_margin)
        new_margin.loc[value] = 1
        clique['belief'] = clique['belief'] / old_margin * new_margin
        clique['belief'].fillna(0)
        self._calibrate_downward(None, clique, 1)

    def _calibrate(self) -> None:
        root = self.root()
        # Upward phase
        root['belief'] = self._calibrate_upward(None, root)
        # Downward phase
        self._calibrate_downward(None, root, 1)

    def _calibrate_upward(self, source: Node, target: Node) -> xa.DataArray:
        if target['type'] == 'separator':
            # Pass the message down in the tree
            clique = target.neighbors().difference({source})[0]
            message = self._calibrate_upward(target, clique)
            # Save the returning message
            target['belief'] = message
            return message
        # Gather the messages
        message = [
            self._calibrate_upward(target, node)
            for node in target.neighbors().difference({source})
        ]
        # Compute the clique belief
        message = reduce(lambda a, b: a * b, message, 1)
        target['belief'] = target['potential'] * message
        if isinstance(target['belief'], int):
            return target['belief']
        # Compute the message
        marginal = target['nodes']
        if source is not None:
            marginal = source['nodes']
        return target['belief'].sum(set(target['belief'].dims) - set(marginal))

    def _calibrate_downward(self, source: Node, target: Node, message: xa.DataArray) -> None:
        if target['type'] == 'separator':
            message = message.sum(set(message.dims) -
                                  set(target['nodes'])) / target['belief']
            # Compute sepset belief
            target['belief'] = target['belief'] * message
            # Pass the message down in the tree
            clique = target.neighbors().difference({source})[0]
            self._calibrate_downward(target, clique, message)
        if target['type'] == 'clique':
            # Compute the final belief
            target['belief'] = target['belief'] * message
            # Propagate the belief
            for node in target.neighbors().difference({source}):
                self._calibrate_downward(target, node, target['belief'])

    def _build_junction_tree(self, network: BayesianNetwork, chain: List) -> Node:
        chain = [tuple(clique) for clique in chain]
        cliques_cpts = self._assign_cpts(network, chain)
        nodes = {
            clique: self._node_from_clique(
                network, clique, cliques_cpts[clique])
            for clique in chain
        }
        # Build Junction Tree from the chain
        n = len(chain)
        # For each clique in the chain
        root = nodes[chain[0]]
        for i in range(1, n):
            Ci = chain[i]
            Ck = self._max_common_clique(chain[:i], Ci)
            self._add_separator(network, nodes[Ck], nodes[Ci])
        return root

    def _assign_cpts(self, network: BayesianNetwork, chain: List) -> Dict:
        cpts = {}
        nodes = set(network.nodes)
        for clique in chain:
            assigned = {
                node
                for node in nodes
                if set(network.family(node)).issubset(clique)
            }
            cpts[clique] = [
                network(node)
                for node in assigned
            ]
            nodes = nodes.difference(assigned)
        return cpts

    def _node_from_clique(self, network: BayesianNetwork, clique: List, cpts: List) -> Node:
        items = OrderedSet(clique)
        node = Node(str(items))
        node['type'] = 'clique'
        node['nodes'] = items
        node['potential'] = reduce(lambda a, b: a * b, cpts, 1)
        return node

    def _max_common_clique(self, chain: List, Ci: Tuple) -> List:
        maxs = [set(Ci).intersection(set(clique)) for clique in chain]
        maxs = [len(common) for common in maxs]
        return chain[maxs.index(max(maxs))]

    def _add_separator(self, network: BayesianNetwork, parent: Node, child: Node) -> None:
        separator_nodes = set(parent['nodes']).intersection(
            set(child['nodes']))
        separator_label = parent.label() + '_' + str(separator_nodes) + '_' + child.label()
        separator = Node(separator_label)
        separator.set_parent(parent)
        child.set_parent(separator)
        separator['type'] = 'separator'
        separator['nodes'] = OrderedSet(separator_nodes)
