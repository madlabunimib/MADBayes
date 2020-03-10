from typing import List, Tuple
from ..structures import DirectedGraph, Node, JunctionTree


def build_junction_tree(graph: DirectedGraph, chain: List) -> JunctionTree:
    # chain = reversed(chain)
    chain = [tuple(clique) for clique in chain]
    nodes = {clique: _node_from_clique(graph, clique) for clique in chain}
    # Build Junction Tree from the chain
    n = len(chain)
    # For each clique in the chain
    root = nodes[chain[0]]
    for i in range(1, n):
        Ci = chain[i]
        Ck = _max_common_clique(chain[:i], Ci)
        _add_separator(graph, nodes[Ck], nodes[Ci])
    junction_tree = JunctionTree(root)
    return junction_tree

def _node_from_clique(graph: DirectedGraph, clique: List) -> Node:
    items = list(clique)
    node = Node(str(items))
    node['type'] = 'clique'
    node['nodes'] = items
    node['clique'] = graph.subgraph(items)
    return node

def _max_common_clique(chain: List, Ci: Tuple) -> List:
    maxs = [set(Ci).intersection(set(clique)) for clique in chain]
    maxs = [len(common) for common in maxs]
    return chain[maxs.index(max(maxs))]

def _add_separator(graph: DirectedGraph, parent: Node, child: Node) -> None:
    separator_nodes = list(set(parent['nodes']).intersection(set(child['nodes'])))
    separator_label = parent.get_label() + '_' + str(separator_nodes) + '_' + child.get_label()
    separator = Node(separator_label)
    separator.set_parent(parent)
    child.set_parent(separator)
    separator['type'] = 'separator'
    separator['nodes'] = separator_nodes
    separator['clique'] = graph.subgraph(separator_nodes)
