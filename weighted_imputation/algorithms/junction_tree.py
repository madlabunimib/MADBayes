from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import networkx as nx

from ..structures import JunctionTree, Node
from .chain_of_cliques import chain_of_cliques
from .moralize import moralize
from .nodes import subgraph
from .triangulate import triangulate

if TYPE_CHECKING:
    from typing import Dict, List, Tuple
    from ..structures import BayesianNetwork


def junction_tree(network: BayesianNetwork) -> JunctionTree:
    moralized = moralize(network)
    triangulated = triangulate(moralized)
    chain = chain_of_cliques(triangulated)
    root = _build_junction_tree(network, chain)
    jt = JunctionTree(root)
    return jt

def _build_junction_tree(network: BayesianNetwork, chain: List) -> Node:
    chain = [tuple(clique) for clique in chain]
    nodes = {clique: _node_from_clique(network, clique) for clique in chain}
    # Build Junction Tree from the chain
    n = len(chain)
    # For each clique in the chain
    root = nodes[chain[0]]
    for i in range(1, n):
        Ci = chain[i]
        Ck = _max_common_clique(chain[:i], Ci)
        _add_separator(network, nodes[Ck], nodes[Ci])
    return root

def _node_from_clique(network: BayesianNetwork, clique: List) -> Node:
    items = list(clique)
    node = Node(str(items))
    node['type'] = 'clique'
    node['nodes'] = items
    node['clique'] = subgraph(network, items, attributes=False)
    return node

def _max_common_clique(chain: List, Ci: Tuple) -> List:
    maxs = [set(Ci).intersection(set(clique)) for clique in chain]
    maxs = [len(common) for common in maxs]
    return chain[maxs.index(max(maxs))]

def _add_separator(network: BayesianNetwork, parent: Node, child: Node) -> None:
    separator_nodes = list(set(parent['nodes']).intersection(set(child['nodes'])))
    separator_label = parent.label() + '_' + str(separator_nodes) + '_' + child.label()
    separator = Node(separator_label)
    separator.set_parent(parent)
    child.set_parent(separator)
    separator['type'] = 'separator'
    separator['nodes'] = separator_nodes
    separator['clique'] = subgraph(network, separator_nodes, attributes=False)

def _assign_cpts_to_cliques():
    pass
